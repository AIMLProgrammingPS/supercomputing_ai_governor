"""
NUMTA 2026 / Operations Research Forum Alignment
Track: Numerical Simulation in OR & Resource Allocation and Scheduling
Description: Core Discrete-Event Simulation Loop that executes workflows 
             under dynamic hardware resource scaling constraints.
"""

import time
import random
from src.engine.resource_governor.py import SimulationWorkloadGovernor # Ensure path alignment

def run_resource_constrained_simulation():
    # Instantiate governor assuming a standard 4-core, 16GB/s bandwidth system
    governor = SimulationWorkloadGovernor(available_cores=4, memory_bandwidth_gbps=16.0)
    
    print("[Simulation Engine] Starting stochastic task loop...")
    
    # Simulate 5 discrete clock cycles of fluctuating system load
    for cycle in range(1, 6):
        # Generate random system metrics to simulate hardware uncertainty
        simulated_cpu_load = random.uniform(50.0, 95.0)
        simulated_pending_tasks = random.randint(1000, 7000)
        
        # Query the AI governor for the optimal execution strategy
        current_policy = governor.determine_execution_policy(
            current_cpu_load=simulated_cpu_load, 
            total_pending_tasks=simulated_pending_tasks
        )
        
        print(f"\n--- Simulation Cycle {cycle} ---")
        print(f"System State -> CPU Load: {simulated_cpu_load:.2f}%, Tasks Pending: {simulated_pending_tasks}")
        print(f"Governor Policy -> Mode: {current_policy['execution_mode']}, Cores Allocated: {current_policy['allocated_cores']}, Step Scale: {current_policy['approximation_scale']}")
        
        # Simulate execution step duration
        time.sleep(0.5)

if __name__ == "__main__":
    run_resource_constrained_simulation()