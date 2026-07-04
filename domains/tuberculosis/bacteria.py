import random
import math
import uuid
from core.agent import Agent
from engine.grn.mutation import GRNMutation
from domains.tuberculosis.tb_genome import TB_GENE_BOUNDS
from evolution.mutation import gaussian_mutate
from domains.tuberculosis.tb_grn import TBGRN
from domains.tuberculosis.tb_metabolism import TBMetabolism
import copy
from domains.tuberculosis.tb_grn_network import REGULATORY_NETWORK
from engine.hyperneat.decoder import HyperNEATDecoder
from engine.hyperneat.cppn import CPPN


class Bacteria(Agent):

    ACTIVE = "ACTIVE"

    STRESSED = "STRESSED"

    DORMANT = "DORMANT"

    REACTIVATING = "REACTIVATING"

    DEAD = "DEAD"


    def __init__(self, x, y, genome=None, config=None):

        super().__init__()

        self.config = config

        self.id = uuid.uuid4().hex[:8]

        self.x = x

        self.y = y

        if genome is None:
         self.genome = {

            "replication_rate": random.uniform(
                self.config["bacteria"]["replication_min"],

                self.config["bacteria"]["replication_max"]
            ),

            "inh_resistance": random.uniform(0,0.1),

            "rif_resistance": random.uniform(0,0.1),

            "fluoroquinolone_resistance": random.uniform(0,0.1),

            "injectable_resistance": random.uniform(0,0.1),

            "dormancy_tendency": random.uniform(0,1),

            "virulence": random.uniform(0,1),

            # -------- GRN genes --------

            "dosR_sensitivity": random.uniform(0.8,1.2),

            "stress_sensitivity": random.uniform(0.8,1.2),

            "growth_sensitivity": random.uniform(0.8,1.2),

            "cppn" : CPPN(),

            "grn_weights": {}

         }

        else:

            self.genome = genome

        if not self.genome["grn_weights"]:

            decoder = HyperNEATDecoder(cppn=self.genome["cppn"])

            self.genome["grn_weights"] = decoder.generate_grn()

        self.state = "ACTIVE"

        self.energy = self.config["bacteria"]["initial_energy"]

        self.fitness = 0.0

        self.age = 0

        self.generation = 0

        self.parent_id = None

        self.children = []

        self.mutations = []

        self.birth_tick = 0

        self.founder_id = self.id

        self.lineage_color = (

            random.randint(50,255),

            random.randint(50,255),

            random.randint(50,255)

        )

        self.grn = TBGRN(self.genome)

        self.metabolism = TBMetabolism()

    def move(self, oxygen_field):

        best_angle = None 
        best_oxygen = -1 
        
        for _ in range(8): 
            angle = random.uniform(0, 2*math.pi) 
            
            test_x = self.x + math.cos(angle) * 10 
            test_y = self.y + math.sin(angle) * 10 
            
            o2 = oxygen_field.oxygen_at( test_x, test_y ) 
            
            if o2 > best_oxygen: 
                best_oxygen = o2 
                best_angle = angle

        if best_angle is not None:

            step = 2

            self.x += math.cos(best_angle) * step
            self.y += math.sin(best_angle) * step

        self.x = max(0, min(self.x, oxygen_field.width - 1))
        self.y = max(0, min(self.y, oxygen_field.height - 1))

    def reproduce(self, world):

        if self.state not in (
            Bacteria.ACTIVE,
            Bacteria.REACTIVATING
        ):
            return None

        fitness_factor = min(2.0, self.fitness / 15.0)

        probability = (
            self.genome["replication_rate"]
            * self.grn.current_phenotype["growth_factor"]
            * fitness_factor
        )

        probability = max(0.0, min(probability, 0.15))

        # Don't allow severely damaged bacteria to replicate
        if self.metabolism.cell_health < 0.30:
            return None

        fitness_cost = (

            self.genome["inh_resistance"] * 0.3 +

            self.genome["rif_resistance"] * 0.3 +

            self.genome["fluoroquinolone_resistance"] * 0.2 +

            self.genome["injectable_resistance"] * 0.2

        )

        probability *= (1 - fitness_cost * 0.5)

        oxygen = self.grn.inputs["oxygen"]

        probability *= oxygen

        neighbors = world.bacteria_near(
            self.x,
            self.y,
            25
        )

        density_factor = max(
            0.40,
            1 - neighbors / 50
        )

        probability *= density_factor

        if random.random() > probability:

            if self.fitness < 8:

                self.energy -= 0.2

                if self.energy <= 0:

                    self.state = Bacteria.DEAD

            return None

        child_genome = gaussian_mutate(

            self.genome,
            TB_GENE_BOUNDS

        )

        child_genome["cppn"] = copy.deepcopy(

            self.genome["cppn"]

        )

        child_genome["cppn"].mutate()

        decoder = HyperNEATDecoder(

            cppn=child_genome["cppn"]

        )

        child_genome["grn_weights"] = decoder.generate_grn()

        self.energy -= self.config["bacteria"]["birth_energy_cost"]

        if self.energy <= 0:
            self.state = Bacteria.DEAD
            return None

        child = Bacteria(

            self.x + random.randint(-5,5),

            self.y + random.randint(-5,5),

            child_genome,

            config=self.config

        )
        child.parent_id = self.id

        child.generation = (self.generation + 1)

        self.children.append(child.id)

        print(
            f"[Birth] "
            f"{self.id} -> {child.id} "
            f"Generation {child.generation}"
        )

        child.birth_tick = world.tick

        child.founder_id = self.founder_id

        child.lineage_color = (self.lineage_color)

        child.mutations = (self.mutations.copy())

        for gene in self.genome:

            if gene in ("grn_weights", "cppn"):
                continue

            old = self.genome[gene]

            new = child.genome[gene]

            if abs(new - old) > 0.05:

                child.mutations.append(
                    {"gene" : gene, 
                      "delta" : round( new-old, 3), 
                      "generation": child.generation
                    }
                )

        if self.fitness < 8:

            self.energy -= 0.2

            if self.energy <= 0:

                self.state = Bacteria.DEAD

        return child


    def update(self, oxygen_field, treatment, macrophages, immune_cells):

        self.age += 1

        oxygen = oxygen_field.oxygen_at(self.x, self.y)

        immune = 0.0

        for m in macrophages:

            d = math.hypot(
                self.x - m.x,
                self.y - m.y
            )

            if d < 80:

                immune += (1.0 - d / 80)

        immune = min(1.0, immune)

        for cell in immune_cells:

            d = math.hypot(
                self.x - cell.x,
                self.y - cell.y
            )

            if d < 50:

                immune += 0.3 * (1 - d / 50)

        immune = min(1.0, immune)

        nutrient = oxygen

        nitric_oxide = min(1.0, immune * 0.8)

        drug = sum(treatment.values()) / len(treatment)

        self.grn.update(
            oxygen,
            immune=immune,
            drug=drug,
            nutrient=nutrient,
            nitric_oxide=nitric_oxide
        )

        g = self.grn.regulators

        self.metabolism.update(
            self.grn,
            self.grn.inputs
        )

        if self.state == Bacteria.DORMANT:

            self.metabolism.atp += 0.01

        else:

            self.metabolism.atp -= 0.005

        self.metabolism.atp = max(
            0.0,
            min(1.0, self.metabolism.atp)
        )

        stress_cost = (
            0.004 * g["sigH"] +
            0.003 * g["sigE"] +
            0.002 * g["mprA"] +
            0.004 * immune
        )

        self.energy -= stress_cost

        self.metabolism.cell_health -= (

            0.003 * immune

        )

        self.metabolism.cell_health = max(

            0.0,

            self.metabolism.cell_health

        )

        if random.random() < 0.0005:
            print(
                f"O2={oxygen:.2f} "
                f"Imm={immune:.2f} "
                f"Drug={drug:.2f} "
                f"State={self.grn.choose_state(self.metabolism)} "
                f"Scores={self.grn.state_scores(self.metabolism)}"
            )

        self.state = self.grn.choose_state(self.metabolism)

        self.energy += oxygen * 0.12

        self.energy = min(self.energy, 100)

        # Oxygen-driven state transition       

        if self.state == Bacteria.DORMANT:

            self.energy -= (
                0.001 * (1 - self.grn.regulators["dosR"])
            )

            # Slow ATP recovery while dormant
            self.metabolism.atp = min(
                1.0,
                self.metabolism.atp + 0.005
            )

            if self.energy <= 0:
                self.state = Bacteria.DEAD


        self.move(oxygen_field)

        drug_pressure = (
            drug *
            (1.0 - self.grn.functions["efflux"])
        )

        if self.state == Bacteria.ACTIVE:

            self.energy -= (
                0.01 +
                0.15 * drug_pressure
            )

        elif self.state == Bacteria.STRESSED:

            self.energy -= (
                0.005 +
                0.10 * drug_pressure
            )

        elif self.state == Bacteria.DORMANT:

            self.energy -= (
                0.002 +
                0.01 * drug_pressure
            )

        elif self.state == Bacteria.REACTIVATING:

            self.energy -= (
                0.007 +
                0.12 * drug_pressure
            )

        if self.energy <= 0:
            self.state = Bacteria.DEAD

        diversity_bonus = random.uniform(0.95, 1.05)

        self.fitness = (

            0.30 * self.energy
            +
            0.30 * self.grn.current_phenotype["growth_factor"]
            +
            0.20 * self.metabolism.cell_health
            +
            0.20 * self.metabolism.atp

        )

        self.genome["cppn"].fitness = self.fitness

        self.genome["cppn"].age += 1

    @property

    def is_mdr(self):

        return (

        self.genome["inh_resistance"] > 0.7

        and

        self.genome["rif_resistance"] > 0.7

        )
    
    @property

    def is_xdr(self):

        return (

        self.is_mdr

        and

        self.genome["fluoroquinolone_resistance"] > 0.7

        and

        self.genome["injectable_resistance"] > 0.7

        )