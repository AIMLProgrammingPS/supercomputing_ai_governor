"""
The Journal of Supercomputing (Springer Nature)
Track: Simulation-Powered Innovation: Driving the Future of Digital Ecosystems
Description: Robust Resource-Aware Governor solving a linear optimization counterpart,
             incorporating dynamic severity scaling directly into bounds constraints.
"""

import numpy as np
from scipy.optimize import linprog
from src.governor.agent import GovernorAgent
from src.utils.logger import log_event

class SimulationWorkloadGovernor:
    def __init__(self, available_cores: int, memory_bandwidth_gbps: float, gamma: float = 0.00):
        self.max_cores = available_cores
        self.max_bandwidth = memory_bandwidth_gbps
        self.agent = GovernorAgent()
        self.gamma = gamma  # Budget of uncertainty parameter

    def determine_execution_policy(self, current_cpu_load: float, total_pending_tasks: int) -> dict:
        execution_mode, smooth_cpu, smooth_task = self.agent.evaluate_system_state(current_cpu_load, total_pending_tasks)
        
        policy = {
            "execution_mode": execution_mode,
            "allocated_cores": self.max_cores,
            "approximation_scale": 1.0,
            "optimized_efficiency": 0.0,
            "smoothed_cpu": round(smooth_cpu, 2),
            "smoothed_task": round(smooth_task, 2)
        }
        
        if execution_mode == "APPROXIMATED_DISCRETE_MILP":
            # Dynamic Severity-Dependence based on exact threshold overrun distance
            severity_factor = min(1.0, max(0.0, (smooth_cpu - self.agent.cpu_threshold) / (100.0 - self.agent.cpu_threshold + 1e-5)))
            min_core_bound = max(0.1, 0.4 - (0.3 * severity_factor))
            max_core_bound = max(0.2, 0.7 - (0.3 * severity_factor))
            
            # Objective: Maximize throughput components -> Minimize negative values
            c = [-1.0, -1.0, 0.0, 0.0]  
            
            # Polyhedral Robust Constraint Array Matrix
            A = [
                [1.0, 1.0, self.gamma, self.gamma],
                [1.0, 0.0, -1.0, 0.0],
                [0.0, 1.0, 0.0, -1.0]
            ]
            b = [0.85, 0.0, 0.0]
            
            bounds = [
                (min_core_bound, max_core_bound),  # Dynamically computed core scale vector bounds
                (0.1, 0.7),                        
                (0.0, None),                       
                (0.0, None)                        
            ]
            
            res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")
            
            if res.success:
                core_fraction, bw_fraction, _, _ = res.x
                policy["allocated_cores"] = max(1, int(self.max_cores * core_fraction))
                policy["approximation_scale"] = float(round(bw_fraction, 2))
                policy["optimized_efficiency"] = float(round(-res.fun, 4))
            else:
                policy["allocated_cores"] = max(1, int(self.max_cores * 0.1))
                policy["approximation_scale"] = 0.1
                policy["optimized_efficiency"] = 0.10
                
        return policy