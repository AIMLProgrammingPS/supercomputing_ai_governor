"""
The Journal of Supercomputing (Springer Nature)
Section: Artificial Intelligence
Track: Intelligent Resource Scheduling and Robust Optimization
Description: Robust Resource-Aware Workload Governor using a Tractable Robust 
             Linear Programming Counterpart to optimally distribute resource 
             fractions under stochastic system background noise.
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
        self.gamma = gamma # Budget of uncertainty parameter

    def determine_execution_policy(self, current_cpu_load: float, total_pending_tasks: int) -> dict:
        execution_mode = self.agent.evaluate_system_state(current_cpu_load, total_pending_tasks)
        
        policy = {
            "execution_mode": execution_mode,
            "allocated_cores": self.max_cores,
            "approximation_scale": 1.0,
            "optimized_efficiency": 1.0
        }
        
        if execution_mode == "APPROXIMATED_DISCRETE_MILP":
            log_event("info", f"Executing real-time Tractable Robust LP solver allocation (Gamma={self.gamma})...")
            
            # Decision Vector v = [x1, x2, z1, z2]^T
            # Objective: Minimize -x1 - x2 + 0*z1 + 0*z2 (Maximize throughput utility fractions)
            c = [-1.0, -1.0, 0.0, 0.0]
            
            # Constraints: A_ub * v <= b_ub
            # Row 1: x1 + x2 + Gamma*z1 + Gamma*z2 <= 0.85 (Joint physical capacity constraint)
            # Row 2: x1 - z1 <= 0  ==>  1*x1 + 0*x2 - 1*z1 + 0*z2 <= 0
            # Row 3: x2 - z2 <= 0  ==>  0*x1 + 1*x2 + 0*z1 - 1*z2 <= 0
            A = [
                [1.0, 1.0, self.gamma, self.gamma],
                [1.0, 0.0, -1.0, 0.0],
                [0.0, 1.0, 0.0, -1.0]
            ]
            b = [0.85, 0.0, 0.0]
            
            # Variable Bounds:
            # 0.1 <= x1, x2 <= 0.7 (Core & Bandwidth allocation limits under stress)
            # 0.0 <= z1, z2 <= inf (Non-negative epigraph auxiliary boundaries)
            bounds = [
                (0.1, 0.7),   # x1 bounds
                (0.1, 0.7),   # x2 bounds
                (0.0, None),  # z1 bounds
                (0.0, None)   # z2 bounds
            ]
            
            res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")
            
            if res.success:
                core_fraction, bw_fraction, z1_val, z2_val = res.x
                policy["allocated_cores"] = max(1, int(self.max_cores * core_fraction))
                policy["approximation_scale"] = float(round(bw_fraction, 2))
                policy["optimized_efficiency"] = float(round(-res.fun, 2))
            else:
                # Safe Fallback under optimization failure
                policy["allocated_cores"] = max(1, int(self.max_cores * 0.1))
                policy["approximation_scale"] = 0.1
                policy["optimized_efficiency"] = 0.2
                
        return policy