import random
import math
from domains.tuberculosis.tb_parameters import TB_PARAMETERS
from engine.grn.gene import Gene
from engine.grn.connection import Connection
from engine.grn.network import GRNNetwork

class TBGRN:

    def __init__(self, genome):

        # Store genome for later use
        self.genome = genome

        self.oxygen = 1.0

        self.regulators = {
            "dosR": 0.0,          # Dormancy regulator
            "sigH": 0.0,          # Oxidative stress response
            "sigE": 0.0,          # Cell envelope stress
            "whiB3": 0.0,         # Redox sensing
            "phoP": 0.5,          # Virulence regulation
            "mprA": 0.0
        }   

        self.genes = {}

        for name, value in self.regulators.items():

            gene = Gene(

                name,

                expression=value,

                decay=TB_PARAMETERS["regulator_decay"]

            )

            self.genes[name] = gene

        self.connections = []

        for source, targets in genome["grn_weights"].items():

            for target, weight in targets.items():

                if target not in self.genes:
                    continue

                c = Connection(
                    self.genes[source],
                    self.genes[target],
                    weight
                )

                self.connections.append(c)

                self.genes[source].add_outgoing(c)

                self.genes[target].add_incoming(c)  

        if len(self.connections) == 0:

            raise RuntimeError("GRN contains no regulatory connections.")

        self.network = GRNNetwork(self.genes, self.connections) 
                
        self.functions = {
            "growth": 1.0,
            "replication": 1.0,
            "efflux": 0.0
        }

        self.physiology = {
            "energy": 1.0,
            "metabolism": 1.0,
            "cell_wall": 1.0,
            "redox_balance": 1.0

        }       

        self.current_phenotype = {
            "growth_factor": 0.0,
            "stress_tolerance": 0.0,
            "dormancy": 0.0,
            "virulence": 0.0,
            "drug_efflux": 0.0,
            "persistence": 0.0
        }

        self.last_state = "ACTIVE"

        self.inputs = {
            "oxygen": 1.0,
            "drug": 0.0,
            "immune": 0.0,
            "nutrient": 1.0,
            "redox":0.0,
            "acidic_pH":0.0,
            "nitric_oxide":0.0,
            "iron_limitation":0.0
        }

        self.sensitivity = {
            "dosR": genome["dosR_sensitivity"],
            "stress": genome["stress_sensitivity"],
            "growth": genome["growth_sensitivity"]
        }

    def update(self, oxygen, drug=0.0, immune=0.0, nutrient=1.0, nitric_oxide=0.0):

        self.oxygen = oxygen

        self.inputs["oxygen"] = oxygen
        self.inputs["drug"] = drug
        self.inputs["immune"] = immune
        self.inputs["nutrient"] = nutrient
        self.inputs["nitric_oxide"] = nitric_oxide

        # ---------- Regulatory interactions ----------

        for _ in range(3):

            external = {}

            for gene in self.genes:

                gene_obj = self.genes[gene]

                momentum = TB_PARAMETERS["regulator_momentum"]

                external[gene] = (

                    momentum * gene_obj.expression

                    +

                    (1 - momentum) * gene_obj.previous_expression

                    +

                    self.environmental_signal(gene)

                )

            self.network.step(external)

            for gene in self.genes.values():

                gene.expression = max(
                    0.0,
                    min(1.0, gene.expression)
                )

        self.regulators = {

            name: gene.expression

            for name, gene in self.genes.items()

        }

        self.update_functions()

        self.update_physiology()

    def phenotype(self, metabolism):

        g = self.regulators

        self.current_phenotype = {

            "growth_factor":

                0.6 * self.functions["growth"]
                + 0.4 * metabolism.atp,

            "stress_tolerance":

                0.4 * (g["sigH"] + g["sigE"])
                + 0.6 * metabolism.cell_health,

            "dormancy":

                0.7 * g["dosR"]
                + 0.3 * (1 - metabolism.atp),

            "virulence":

                0.6 * g["phoP"]
                + 0.4 * metabolism.cell_health,

            "drug_efflux":

                self.functions["efflux"],

            "persistence":

                0.5 * g["mprA"]
                + 0.5 * (1 - metabolism.atp)

        }

        return self.current_phenotype
    
    def state_scores(self, metabolism):

        p = self.phenotype(metabolism)

        scores = {}

        scores["ACTIVE"] = (

            0.60 * p["growth_factor"]
            + 0.25 * self.inputs["oxygen"]
            + 0.15 * self.inputs["nutrient"]

        )

        scores["DORMANT"] = (

            0.55 * p["dormancy"]
            + 0.25 * (1 - self.inputs["oxygen"])
            + 0.20 * p["persistence"]

        )

        scores["STRESSED"] = (

            0.45 * p["stress_tolerance"]

            + 0.30 * self.inputs["drug"]

            + 0.25 * self.inputs["immune"]

        )

        scores["REACTIVATING"] = (

            0.50 * p["growth_factor"]

            + 0.30 * self.inputs["oxygen"]

            + 0.20 * (1 - p["dormancy"])

        )

        return scores
    
    def choose_state(self, metabolism):

        scores = self.state_scores(metabolism)

        ordered = sorted(

            scores.items(),

            key=lambda x: x[1],

            reverse=True

        )

        best_state = ordered[0][0]

        if (
            self.inputs["immune"] > 0.70
            or self.inputs["drug"] > 0.70
        ):
            best_state = "STRESSED"

        if len(ordered) > 1:

            if ordered[0][1] - ordered[1][1] < 0.05:

                best_state = self.last_state

        if self.last_state == "DORMANT":

    # Stay dormant while oxygen is still low
            if self.inputs["oxygen"] < 0.45:

                best_state = "DORMANT"

            elif (
                self.inputs["oxygen"] > 0.70
                and
                metabolism.atp > 0.40
            ):

                best_state = "REACTIVATING"

        self.last_scores = scores

        self.last_state = best_state

        return best_state
        
    def sigmoid(self, x):
            return 1.0 / (1.0 + math.exp(-x))
    
    def environmental_signal(self, gene):

        signal = 0.0

        oxygen = self.inputs["oxygen"]
        immune = self.inputs["immune"]
        drug = self.inputs["drug"]
        redox = self.inputs["redox"]

        if gene == "dosR":

            signal = (
                0.6 * (1.0 - oxygen)
                + 0.4 * self.inputs["nitric_oxide"]
            )

            signal *= (
                TB_PARAMETERS["dosR_activation"]
                * self.sensitivity["dosR"]
            )

        elif gene == "sigH":

            signal = (
                0.9 * immune
                + 0.1 * (1.0 - oxygen)
            ) * TB_PARAMETERS["sigH_activation"]

        elif gene == "sigE":

            signal = (
                0.7 * drug
                + 0.3 * immune
            ) * TB_PARAMETERS["sigE_activation"]

        elif gene == "whiB3":

            signal = (
                0.7 * redox
                + 0.3 * (1.0 - oxygen)
            ) * TB_PARAMETERS["whiB3_activation"]

        elif gene == "mprA":

            signal = (
                0.5 * immune
                + 0.5 * drug
            )

        elif gene == "phoP":

            signal = (
                0.7 * oxygen
                + 0.3 * self.inputs["nutrient"]
            )

        return signal
    
    def update_functions(self):

        r = self.regulators
        f = self.functions

        growth_input = (

            TB_PARAMETERS["growth_bias"]
            + 0.4 * self.inputs["oxygen"]
            + TB_PARAMETERS["growth_dosR_weight"] * r["dosR"]
            + TB_PARAMETERS["growth_sigH_weight"] * r["sigH"]
            + TB_PARAMETERS["growth_mprA_weight"] * r["mprA"]
            + TB_PARAMETERS["growth_phoP_weight"] * r["phoP"]

        )

        energy_factor = (
            0.2 * self.physiology["energy"]
            + 0.8 * self.inputs["oxygen"]
        )

        f["growth"] = (
            self.sigmoid(growth_input)
            * energy_factor
        )

        drug_penalty = 1.0 - 0.30 * self.inputs["drug"]

        f["growth"] *= max(0.0, drug_penalty)

        f["replication"] = f["growth"]

        efflux_input = (

            TB_PARAMETERS["efflux_sigE_weight"]*r["sigE"]

            + TB_PARAMETERS["efflux_mprA_weight"]*r["mprA"]

        )

        f["efflux"] = self.sigmoid(efflux_input)

    def update_physiology(self):

        r = self.regulators

        p = self.physiology

        f = self.functions

        p["metabolism"] = (
            0.7 * f["growth"]
            + 0.3 * (1 - r["dosR"])
        )

        p["energy"] = (
            0.5 * p["metabolism"]
            + 0.3 * self.inputs["nutrient"]
            + 0.2 * self.inputs["oxygen"]
        )

        p["cell_wall"] = (
            0.7
            + 0.3 * r["sigE"]
        )

        p["redox_balance"] = (
            0.5
            + 0.5 * r["whiB3"]
        )