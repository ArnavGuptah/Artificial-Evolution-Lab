from engine.hyperneat.substrate import Substrate
from engine.hyperneat.cppn import CPPN


class HyperNEATDecoder:

    def __init__(self, cppn=None, substrate=None):

        self.cppn = cppn if cppn else CPPN()
        self.substrate = substrate if substrate else Substrate()

    def generate_grn(self):

        grn = {}

        for source in self.substrate.node_names():
            grn[source] = {}

        for source, target in self.substrate.all_connections():

            inputs = self.substrate.cppn_inputs(source, target)

            weight = self.cppn.forward(inputs)

            grn[source][target] = weight

        return grn