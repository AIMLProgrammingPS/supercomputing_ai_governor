"""
The Journal of Supercomputing (Springer Nature)
Section: Artificial Intelligence
Track: Intelligent Resource Scheduling and Robust Optimization
Description: Fault-tolerant configuration loader with robust exception catchers.
"""

import json
import os
from src.utils.logger import log_event

class GovernorAgent:
    def __init__(self, config_path: str = "config/hyperparams.json"):
        self.config_path = config_path
        self.cpu_threshold = 85.0
        self.task_threshold = 5000
        self.load_hyperparameters()

    def load_hyperparameters(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                    thresholds = config.get("hardware_thresholds", {})
                    self.cpu_threshold = float(thresholds.get("max_cpu_utilization_percent", 85.0))
                    self.task_threshold = int(thresholds.get("max_pending_tasks_threshold", 5000))
                log_event("info", f"GovernorAgent successfully parsed hyperparams from {self.config_path}")
            else:
                raise FileNotFoundError("Configuration file is completely missing.")
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            log_event("error", f"Corrupt config file! Falling back to safe defaults. Error: {e}")
            self.cpu_threshold = 85.0
            self.task_threshold = 5000
        except Exception as e:
            log_event("error", f"Unexpected structural error: {e}. Loading safe operational state.")
            self.cpu_threshold = 85.0
            self.task_threshold = 5000

    def evaluate_system_state(self, cpu_load: float, pending_tasks: int) -> str:
        if cpu_load > self.cpu_threshold or pending_tasks > self.task_threshold:
            return "APPROXIMATED_DISCRETE_MILP"
        return "HIGH_FIDELITY_CONTINUOUS"