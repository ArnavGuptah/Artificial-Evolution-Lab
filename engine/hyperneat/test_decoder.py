from engine.hyperneat.decoder import HyperNEATDecoder

decoder = HyperNEATDecoder()

grn = decoder.generate_grn()

print("\nGenerated GRN\n")

for source in grn:

    print(source)

    for target in grn[source]:

        print(f" {target}: {grn[source][target]:.3f}")