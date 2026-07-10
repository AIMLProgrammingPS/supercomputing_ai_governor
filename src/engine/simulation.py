"""
NUMTA 2026 / Operations Research Forum Alignment
Track: Numerical Simulation in OR & Resource Allocation and Scheduling
Description: Core Discrete-Event Simulation Loop that executes workflows 
             under dynamic hardware resource scaling constraints.
"""

import time
import random
from src.engine.resource_governor import SimulationWorkloadGovernor
from src.utils.logger import log_event

def run_resource_constrained_simulation():
    governor = SimulationWorkloadGovernor(available_cores=4, memory_bandwidth_gbps=16.0)
    
    log_event("info", "Starting resource-constrained stochastic task loop...")
    
    for cycle in range(1, 6):
        simulated_cpu_load = random.uniform(50.0, 95.0)
        simulated_pending_tasks = random.randint(1000, 7000)
        
        current_policy = governor.determine_execution_policy(
            current_cpu_load=simulated_cpu_load, 
            total_pending_tasks=simulated_pending_tasks
        )
        
        log_event("info", f"Cycle {cycle} State -> CPU: {simulated_cpu_load:.1f}%, Tasks: {simulated_pending_tasks}")
        log_event("status", f"Governor Action -> Mode: {current_policy['execution_mode']}, Step Scale: {current_policy['approximation_scale']}")
        
        time.sleep(0.3)

if __name__ == "__main__":
    run_resource_constrained_simulation()