from evolution.mutation_strategy import MutationStrategy
from evolution.mutation import gaussian_mutate

class GaussianMutationStrategy(MutationStrategy):

    def mutate_genome(self, genome, bounds):
        return gaussian_mutate(genome, bounds)

    def mutate_cppn(self, cppn, speciation, stress, parent):

        from evolution.adaptive_mutation import AdaptiveMutation

        rate, sigma = speciation.mutation_rate(cppn)

        mult = AdaptiveMutation.stress_multiplier(parent)

        rate *= mult
        sigma *= mult

        rate *= (1 + stress)
        sigma *= (1 + 0.5 * stress)

        rate = min(rate, 0.40)
        sigma = min(sigma, 0.50)

        cppn.mutate(
            mutation_rate=rate,
            sigma=sigma
        )