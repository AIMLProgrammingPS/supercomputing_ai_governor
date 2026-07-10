"""
NUMTA 2026 / Operations Research Forum Alignment
Track: Parallel and Distributed Computing in OR & Resource Allocation
Description: Resource-Aware Workload Governor using Linear Programming
             to optimally distribute resource fractions under system stress.
"""

import numpy as np
from scipy.optimize import linprog
from src.governor.agent import GovernorAgent
from src.utils.logger import log_event

class SimulationWorkloadGovernor:
    def __init__(self, available_cores: int, memory_bandwidth_gbps: float):
        self.max_cores = available_cores
        self.max_bandwidth = memory_bandwidth_gbps
        self.agent = GovernorAgent()
        
    def determine_execution_policy(self, current_cpu_load: float, total_pending_tasks: int) -> dict:
        execution_mode = self.agent.evaluate_system_state(current_cpu_load, total_pending_tasks)
        
        policy = {
            "execution_mode": execution_mode,
            "allocated_cores": self.max_cores,
            "approximation_scale": 1.0,
            "optimized_efficiency": 1.0
        }
        
        if execution_mode == "APPROXIMATED_DISCRETE_MILP":
            log_event("info", "Executing real-time Scipy Linear Programming solver allocation...")
            # Objective: Maximize resource utility fraction (minimize negative utility)
            c = [-1.0, -1.0] # Weights for [Core Allocation Fraction, Bandwidth Allocation Fraction]
            
            # Constraints: Cores + Bandwidth fractions <= 1.0 (normalized stress bound)
            A = [[1.0, 1.0]]
            b = [0.85] # Bound to 85% utilization cap
            
            # Bounds for fractions (min 10% allocation, max 70% allocation under stress)
            x_bounds = (0.1, 0.7)
            y_bounds = (0.1, 0.7)
            
            res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method="highs")
            
            if res.success:
                core_fraction, bw_fraction = res.x
                policy["allocated_cores"] = max(1, int(self.max_cores * core_fraction))
                policy["approximation_scale"] = float(round(bw_fraction, 2))
                policy["optimized_efficiency"] = float(round(-res.fun, 2))
            else:
                # Safe Fallback
                policy["allocated_cores"] = max(1, int(self.max_cores * 0.5))
                policy["approximation_scale"] = 0.1
                
        return policy