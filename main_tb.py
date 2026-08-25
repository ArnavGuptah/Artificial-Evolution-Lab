import sys
from configs.config_loader import ConfigLoader
from core.experiment.experiment_manager import ExperimentManager
from domains.tuberculosis.tb_world import TBWorld
import argparse


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "experiment",
        nargs="?",
        default="baseline"
    )

    parser.add_argument(
        "--backend",
        choices=["qsvm", "vqc"],
        default="qsvm"
    )

    args = parser.parse_args()

    mode = args.experiment
    backend = args.backend

    if mode == "all":

        experiments = [

            "baseline",
            "hypoxia",
            "hyperoxia",
            "treatment",
            "immune_high"

        ]

        results = {}

        for experiment in experiments:

            print(f"\nRunning {experiment}...")

            try:
                run_experiment(experiment, backend)
                results[experiment] = "PASS"
                print(f"✓ {experiment} completed")

            except Exception as e:
                results[experiment] = "FAIL"
                print(f"✗ {experiment} failed")
                print(e)

        print("\n========== SUMMARY ==========")

        for name, status in results.items():
            print(f"{name:15s} {status}")

        print("\n========== SUMMARY ==========")

        for experiment, status in results.items():

            print(f"{experiment:<15}{status}")

        print("=============================")

        return

    run_experiment(mode, backend)

def run_experiment(config_name, backend):

    config = ConfigLoader(
        "tuberculosis",
        config_name
    )

    manager = ExperimentManager(config_name, config)

    manager.prepare()

    manager.save_config()

    manager.save_metadata()

    log_file = open(
        manager.log_path(),
        "w",
        encoding="utf-8"
    )

    original_stdout = sys.stdout

    try:

        sys.stdout = log_file

        world = TBWorld(
            config,
            manager,
            backend=backend
        )

        world.run()

    finally:

        sys.stdout = original_stdout

        log_file.close()

if __name__ == "__main__":
    main()