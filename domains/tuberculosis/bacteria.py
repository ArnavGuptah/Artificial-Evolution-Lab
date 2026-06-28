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


class Bacteria(Agent):

    ACTIVE = "ACTIVE"

    STRESSED = "STRESSED"

    DORMANT = "DORMANT"

    REACTIVATING = "REACTIVATING"

    DEAD = "DEAD"


    def __init__(self, x, y, genome=None):

        super().__init__()

        self.id = uuid.uuid4().hex[:8]

        self.x = x

        self.y = y

        if genome is None:
         self.genome = {

            "replication_rate": random.uniform(0.002,0.01),

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

            "grn_weights": {}

         }

        else:

            self.genome = genome

        if not self.genome["grn_weights"]:

            for source, targets in REGULATORY_NETWORK.items():

                self.genome["grn_weights"][source] = {}

                for target in targets:

                    self.genome["grn_weights"][source][target] = random.uniform(-1.0,1.0)

        self.state = "ACTIVE"

        self.energy = 50

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


    def reproduce(self, world):

        if self.state not in (
            Bacteria.ACTIVE,
            Bacteria.REACTIVATING
        ):
            return None

        phenotype = self.grn.phenotype(self.metabolism)

        probability = (self.genome[ "replication_rate"] * self.grn.current_phenotype["growth_factor"] * 5.0)

        probability = min(probability, 0.10)

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
            0.15,
            1 - neighbors / 35
        )

        probability *= density_factor

        if random.random() < 0.0005:
            print(
                f"[REPRO] ID={self.id} "
                f"State={self.state} "
                f"Prob={probability:.5f} "
                f"Growth={self.grn.current_phenotype['growth_factor']:.3f} "
                f"Energy={self.energy:.1f}"
                f"Density={neighbors} "
                f"Factor={density_factor:.2f}"
            )

        if random.random() > probability:

            return None


        child_genome = gaussian_mutate(

            self.genome,
            TB_GENE_BOUNDS

        )

        self.energy -= 20

        if self.energy <= 0:
            self.state = Bacteria.DEAD
            return None

        child = Bacteria(

            self.x + random.randint(-5,5),

            self.y + random.randint(-5,5),

            child_genome

        )

        GRNMutation.mutate_connections(child.grn.connections)

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

            if gene == "grn_weights":
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

        return child


    def update(self, oxygen_field):

        self.age += 1

        oxygen = oxygen_field.oxygen_at(self.x, self.y)

        self.grn.update(oxygen)

        g = self.grn.regulators

        self.metabolism.update(

            self.grn,

            self.grn.inputs

        )

        stress_cost = (
            0.003 * g["sigH"] +
            0.003 * g["sigE"] +
            0.002 * g["mprA"]
        )

        self.energy -= stress_cost

        if random.random() < 0.001:
            print(
                "O2:",
                round(oxygen, 2),
                "dosR:",
                round(self.grn.regulators["dosR"], 2),
                "growth:",
                round(self.grn.functions["growth"], 2),
                "sigH:",
                round(self.grn.regulators["sigH"], 2),
                "sigE:",
                round(self.grn.regulators["sigE"], 2)
            )

        phenotype = self.grn.phenotype(self.metabolism)

        if phenotype["dormancy"] > 0.80:

            self.state = Bacteria.DORMANT

        elif (
            phenotype["stress_tolerance"] > 0.75
            and self.grn.inputs["immune"] > 0.30
        ):

            self.state = Bacteria.STRESSED

        elif (
            phenotype["growth_factor"] > 0.45
        ):

            self.state = Bacteria.ACTIVE

        else:

            self.state = Bacteria.REACTIVATING

        self.energy += oxygen * 0.12

        self.energy = min(self.energy, 100)

        # Oxygen-driven state transition       

        if self.state == Bacteria.DORMANT:

                self.energy -= (0.002 * (1 - self.grn.regulators["dosR"]))

                if self.energy <= 0:

                    self.state = Bacteria.DEAD

                return


        self.move(oxygen_field)

        if self.state == Bacteria.ACTIVE:
            loss = 0.01

            loss *= (
                1 - 0.3 * self.grn.regulators["mprA"]
            )

            self.energy -= loss

        elif self.state == Bacteria.STRESSED:
            self.energy -= 0.005

        elif self.state == Bacteria.REACTIVATING:
            self.energy -= 0.007

        if self.energy <= 0:
            self.state = Bacteria.DEAD

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