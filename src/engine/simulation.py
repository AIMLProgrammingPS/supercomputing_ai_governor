"""
The Journal of Supercomputing (Springer Nature)
Section: Artificial Intelligence
Description: Verification execution harness logging robust metrics over a 15-cycle horizon.
"""

import time
import random
import csv
import os
from src.engine.resource_governor import SimulationWorkloadGovernor
from src.utils.logger import log_event

def run_resource_constrained_simulation():
    # Instantiates baseline tracking governor (Gamma=0.00)
    governor = SimulationWorkloadGovernor(available_cores=8, memory_bandwidth_gbps=32.0, gamma=0.00)
    log_event("info", "Starting resource-constrained robust task validation loop...")
    
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    csv_path = os.path.join(log_dir, "telemetry.csv")
    
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Cycle", "CPULoad", "PendingTasks", "Mode", "Cores", "Scale", "Efficiency"])
        
        for cycle in range(1, 16):
            simulated_cpu_load = random.uniform(40.0, 98.0)
            simulated_pending_tasks = random.randint(800, 8000)
            
            current_policy = governor.determine_execution_policy(
                current_cpu_load=simulated_cpu_load, 
                total_pending_tasks=simulated_pending_tasks
            )
            
            writer.writerow([
                cycle, simulated_cpu_load, simulated_pending_tasks, 
                current_policy['execution_mode'], current_policy['allocated_cores'], 
                current_policy['approximation_scale'], current_policy['optimized_efficiency']
            ])
            
            log_event("info", f"Cycle {cycle} -> Mode: {current_policy['execution_mode']}...")

if __name__ == "__main__":
    run_resource_constrained_simulation()