class Comparator:

    @staticmethod
    def compare(baseline, experiment, experiment_name):

        print("\n========== EXPERIMENT COMPARISON ==========\n")

        metrics = [

            ("Population", "Population"),
            ("Active%", "Active%"),
            ("Dormant%", "Dormant%"),
            ("Stress%", "Stress%"),
            ("Average Fitness", "AverageFitness"),
            ("Average ATP", "AverageATP"),
            ("Average Growth", "AverageGrowth"),
            ("Average DosR", "AverageDosR"),
            ("Species", "Species"),
            ("Largest Species", "LargestSpecies"),
            ("Average Species Size", "AverageSpeciesSize"),
            ("Generation", "Generation"),
            ("Living Lineages", "LivingLineages"),
            ("Average Novelty", "AverageNovelty"),
            ("Pareto Fronts", "ParetoFronts"),
            ("Best Front Size", "BestFrontSize"),
            ("Average Pareto Rank", "AverageParetoRank")

        ]

        for name, column in metrics:

            baseline_value = float(baseline.get(column, 0))
            experiment_value = float(experiment.get(column, 0)
)

            difference = experiment_value - baseline_value

            if abs(baseline_value) > 1e-6:

                percent = (100 * difference / baseline_value)

            else:

                percent = 0.0

            print(f"  Change : {percent:+.1f}%")

            if abs(percent) > 20:

                print("  *** Significant Change ***")

            print(f"{name}")

            print(f"  Baseline : {baseline_value:.2f}")
            print(f"  {experiment_name} : {experiment_value:.2f}")
            print(f"  Difference : {difference:+.2f}")

            print()