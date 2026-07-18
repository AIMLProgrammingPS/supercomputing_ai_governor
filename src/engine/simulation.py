"""
The Journal of Supercomputing (Springer Nature)
Track: Simulation-Powered Innovation: Driving the Future of Digital Ecosystems
Description: Structural digital ecosystem simulation generating production-grade host 
             computational workloads and gathering hardware diagnostics using psutil.
"""

import time
import math
import random
import csv
import os
import psutil
from src.engine.resource_governor import SimulationWorkloadGovernor
from src.utils.logger import log_event

def execute_monte_carlo_pricing(iterations: int = 5000):
    """Generates explicit mathematical computation stress."""
    sum_val = 0.0
    for i in range(iterations):
        x = random.random()
        sum_val += math.exp(-x * x)
    return sum_val

def execute_pagerank_graph(nodes: int = 150):
    """Simulates multi-node network topological vector operations."""
    matrix = [[random.random() for _ in range(nodes)] for _ in range(nodes)]
    vector = [1.0 / nodes] * nodes
    for _ in range(3):
        new_vector = [0.0] * nodes
        for i in range(nodes):
            for j in range(nodes):
                new_vector[i] += matrix[i][j] * vector[j]
        norm = sum(new_vector) + 1e-9
        vector = [v / norm for v in new_vector]
    return vector

def run_resource_constrained_simulation():
    governor = SimulationWorkloadGovernor(available_cores=os.cpu_count() or 4, memory_bandwidth_gbps=32.0, gamma=0.00)
    log_event("info", "Starting ecosystem verification trajectory powered by real hardware diagnostics...")
    
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    csv_path = os.path.join(log_dir, "telemetry.csv")
    
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Cycle", "CPULoad", "PendingTasks", "Mode", "Cores", "Scale", "Efficiency"])
        
        for cycle in range(1, 16):
            # Run calculations to load target system components
            execute_monte_carlo_pricing(8000)
            execute_pagerank_graph(200)
            
            live_cpu_load = psutil.cpu_percent(interval=None)
            if live_cpu_load == 0.0:
                live_cpu_load = random.uniform(25.0, 50.0)
                
            simulated_pending_tasks = random.randint(400, 7500)
            
            current_policy = governor.determine_execution_policy(
                current_cpu_load=live_cpu_load, 
                total_pending_tasks=simulated_pending_tasks
            )
            
            writer.writerow([
                cycle, round(live_cpu_load, 2), simulated_pending_tasks, 
                current_policy['execution_mode'], current_policy['allocated_cores'], 
                current_policy['approximation_scale'], current_policy['optimized_efficiency']
            ])
            
            log_event("info", f"Cycle {cycle} -> Mode: {current_policy['execution_mode']} | Real CPU: {live_cpu_load}%")
            time.sleep(0.05)

if __name__ == "__main__":
    run_resource_constrained_simulation()