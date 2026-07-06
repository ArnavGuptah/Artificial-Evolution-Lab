from pathlib import Path
import json
import shutil
import time
import platform
import hashlib
import sys
import os
from datetime import datetime

class ExperimentManager:

    def __init__(self, experiment_name, config):

        self.name = experiment_name

        self.config = config

        base = Path("experiments") / experiment_name

        base.mkdir(

            parents=True,

            exist_ok=True

        )

        existing = [

            d for d in base.iterdir()

            if d.is_dir()

            and d.name.startswith("run_")

        ]

        run_number = len(existing) + 1

        self.root = base / f"run_{run_number:03d}"

    def prepare(self):

        if self.root.exists():

            shutil.rmtree(self.root)

        self.root.mkdir(
            parents=True,
            exist_ok=True
        )

    def path(self, filename):

        return self.root / filename
    
    def save_config(self):

        with open(self.path("config.json"), "w") as f:

            json.dump(self.config.data, f, indent=4)

    def save_metadata(self):

        metadata = {

            "experiment":

                self.name,

            "timestamp":

                datetime.now().isoformat(),

            "configuration_hash":

                self.configuration_hash()

        }

        with open(

            self.path(

                "metadata.json"

            ),

            "w"

        ) as f:

            json.dump(

                metadata,

                f,

                indent=4

            )

    def log_path(self):

        return self.path("tb_log.txt")
    
    def plots_path(self):

        folder = self.path(

            "plots"

        )

        folder.mkdir(

            exist_ok=True

        )

        return folder
    
    def configuration_hash(self):

        encoded = json.dumps(

            self.config.data,

            sort_keys=True

        ).encode()

        return hashlib.sha256(

            encoded

        ).hexdigest()
    
    def save_environment(self):

        environment = {

            "python":

                sys.version,

            "platform":

                platform.platform(),

            "architecture":

                platform.machine()

        }

        with open(

            self.path(

                "environment.json"

            ),

            "w"

        ) as f:

            json.dump(

                environment,

                f,

                indent=4

            )

    