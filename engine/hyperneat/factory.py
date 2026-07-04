from engine.hyperneat.substrate import TBSubstrate
from engine.hyperneat.cppn import CPPN
from engine.hyperneat.decoder import HyperNEATDecoder


def build_grn(genome):

    substrate = TBSubstrate()

    cppn = CPPN(genome)

    decoder = HyperNEATDecoder(substrate, cppn)

    return decoder.generate_grn()