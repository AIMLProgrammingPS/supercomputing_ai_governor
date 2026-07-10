"""
NUMTA 2026 / Operations Research Forum Alignment
Track: Artificial Intelligence in OR & Machine Learning in OR
Description: Autonomous optimization agent that loads external hyperparameters
             and calculates operational penalty weights dynamically.
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
        """Loads structural execution constraints from the configuration layer."""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                config = json.load(f)
                thresholds = config.get("hardware_thresholds", {})
                self.cpu_threshold = thresholds.get("max_cpu_utilization_percent", 85.0)
                self.task_threshold = thresholds.get("max_pending_tasks_threshold", 5000)
            log_event("info", f"GovernorAgent loaded hyperparams from {self.config_path}")
        else:
            log_event("warn", f"Config not found at {self.config_path}. Using fallback defaults.")

    def evaluate_system_state(self, cpu_load: float, pending_tasks: int) -> str:
        """Applies rule-based optimization choices to govern system execution."""
        if cpu_load > self.cpu_threshold or pending_tasks > self.task_threshold:
            return "APPROXIMATED_DISCRETE_MILP"
        return "HIGH_FIDELITY_CONTINUOUS"