"""
NUMTA 2026 / Operations Research Forum Alignment
Description: Simulation execution harness that logs structured metrics to CSV file.
"""

import time
import random
import csv
import os
from src.engine.resource_governor import SimulationWorkloadGovernor
from src.utils.logger import log_event

def run_resource_constrained_simulation():
    governor = SimulationWorkloadGovernor(available_cores=8, memory_bandwidth_gbps=32.0)
    log_event("info", "Starting resource-constrained extended task loop...")
    
    # Setup CSV tracking path
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    csv_path = os.path.join(log_dir, "telemetry.csv")
    
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Cycle", "CPULoad", "PendingTasks", "Mode", "Cores", "Scale"])
        
        # Simulate an extended 15-cycle operational window
        for cycle in range(1, 16):
            simulated_cpu_load = random.uniform(40.0, 98.0)
            simulated_pending_tasks = random.randint(800, 8000)
            
            current_policy = governor.determine_execution_policy(
                current_cpu_load=simulated_cpu_load, 
                total_pending_tasks=simulated_pending_tasks
            )
            
            writer.writerow([
                cycle, simulated_cpu_load, simulated_pending_tasks, 
                current_policy['execution_mode'], current_policy['allocated_cores'], current_policy['approximation_scale']
            ])
            
            log_event("info", f"Cycle {cycle} -> System Core Strain: {simulated_cpu_load:.1f}%")
            time.sleep(0.1)
            
    log_event("info", f"Telemetry successfully compiled and dumped into {csv_path}")

if __name__ == "__main__":
    run_resource_constrained_simulation()