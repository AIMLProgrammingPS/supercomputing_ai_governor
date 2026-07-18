"""
The Journal of Supercomputing (Springer Nature)
Track: Simulation-Powered Innovation: Driving the Future of Digital Ecosystems
Description: State classification wrapper featuring Exponential Moving Average (EMA) 
             signal filtering to mitigate governor chattering under noisy state inputs.
"""

import json
import os
from src.utils.logger import log_event

class GovernorAgent:
    def __init__(self, config_path: str = "config/hyperparams.json"):
        self.config_path = config_path
        
        # Default operational thresholds
        self.cpu_threshold = 85.0
        self.task_threshold = 5000
        
        # EMA Filter Coefficients (Alpha values between 0 and 1)
        self.alpha_cpu = 0.30
        self.alpha_task = 0.25
        
        # Initializing historical state tracking registers
        self.smoothed_cpu = None
        self.smoothed_task = None
        
        self.load_hyperparameters()

    def load_hyperparameters(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                    thresholds = config.get("hardware_thresholds", {})
                    self.cpu_threshold = float(thresholds.get("max_cpu_utilization_percent", 85.0))
                    self.task_threshold = int(thresholds.get("max_pending_tasks_threshold", 5000))
                    
                    ema_params = config.get("ema_parameters", {})
                    self.alpha_cpu = float(ema_params.get("alpha_cpu", 0.30))
                    self.alpha_task = float(ema_params.get("alpha_task", 0.25))
                    
                log_event("info", f"GovernorAgent successfully parsed hyperparams from {self.config_path}")
            else:
                log_event("info", "Configuration file missing. Utilizing robust internal defaults.")
        except Exception as e:
            log_event("error", f"Error loading config: {e}. Falling back to safe operational state.")
            self.cpu_threshold = 85.0
            self.task_threshold = 5000

    def reset_filter(self):
        """Resets the historical registers to avoid cross-run state bleeding."""
        self.smoothed_cpu = None
        self.smoothed_task = None

    def evaluate_system_state(self, raw_cpu_load: float, raw_pending_tasks: int) -> tuple[str, float, float]:
        """
        Applies a first-order recurrence relation filter (EMA) to eliminate noisy 
        spikes, then classifies execution state based on smoothed tracking.
        """
        if self.smoothed_cpu is None:
            self.smoothed_cpu = raw_cpu_load
        else:
            self.smoothed_cpu = (self.alpha_cpu * raw_cpu_load) + ((1.0 - self.alpha_cpu) * self.smoothed_cpu)
            
        if self.smoothed_task is None:
            self.smoothed_task = float(raw_pending_tasks)
        else:
            self.smoothed_task = (self.alpha_task * float(raw_pending_tasks)) + ((1.0 - self.alpha_task) * self.smoothed_task)

        if self.smoothed_cpu > self.cpu_threshold or self.smoothed_task > self.task_threshold:
            return "APPROXIMATED_DISCRETE_MILP", self.smoothed_cpu, self.smoothed_task
            
        return "HIGH_FIDELITY_CONTINUOUS", self.smoothed_cpu, self.smoothed_task