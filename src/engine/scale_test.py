"""
NUMTA 2026 / Operations Research Forum Alignment
Description: Mass-scale stochastic simulation engine (1,000+ cycles) 
             to generate high-density statistical datasets for analysis.
"""

import csv
import os
import random
from src.engine.resource_governor import SimulationWorkloadGovernor
from src.utils.logger import log_event

def run_large_scale_simulation(total_cycles: int = 1000):
    governor = SimulationWorkloadGovernor(available_cores=8, memory_bandwidth_gbps=32.0)
    log_event("info", f"Initializing high-density simulation matrix: {total_cycles} cycles...")
    
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    csv_path = os.path.join(log_dir, "scale_telemetry.csv")
    
    milp_count = 0
    high_fid_count = 0
    cumulative_efficiency_saved = 0.0
    
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Cycle", "CPULoad", "PendingTasks", "Mode", "EfficiencySaved"])
        
        for cycle in range(1, total_cycles + 1):
            # Generate stochastic system strain vectors
            simulated_cpu_load = random.uniform(30.0, 99.0)
            simulated_pending_tasks = random.randint(500, 9000)
            
            policy = governor.determine_execution_policy(
                current_cpu_load=simulated_cpu_load, 
                total_pending_tasks=simulated_pending_tasks
            )
            
            # Metrics aggregation
            if policy["execution_mode"] == "APPROXIMATED_DISCRETE_MILP":
                milp_count += 1
                # Theoretical saved compute overhead = (1.0 - approximation_scale) * optimization efficiency
                saved_overhead = (1.0 - policy["approximation_scale"]) * policy["optimized_efficiency"]
            else:
                high_fid_count += 1
                saved_overhead = 0.0
                
            cumulative_efficiency_saved += saved_overhead
            
            writer.writerow([
                cycle, round(simulated_cpu_load, 2), simulated_pending_tasks, 
                policy["execution_mode"], round(saved_overhead, 4)
            ])
            
            # Print status update every 200 cycles to monitor progress without spamming
            if cycle % 200 == 0:
                log_event("info", f"Progress Checkpoint -> Completed {cycle}/{total_cycles} cycles...")

    # Calculate final distribution metrics
    milp_ratio = (milp_count / total_cycles) * 100
    avg_efficiency = (cumulative_efficiency_saved / total_cycles) * 100
    
    print("\n" + "="*50)
    print("        NUMTA 2026 STATISTICAL ANALYSIS METRICS")
    print("="*50)
    print(f"Total Simulated Operational Cycles : {total_cycles}")
    print(f"High-Fidelity Continuous Windows   : {high_fid_count}")
    print(f"Approximated LP Mitigations triggered: {milp_count} ({milp_ratio:.1f}%)")
    print(f"Estimated System Efficiency Gained : {avg_efficiency:.2f}% load reduction")
    print("="*50 + "\n")
    
    log_event("info", f"Mass-scale dataset successfully saved to {csv_path}")

if __name__ == "__main__":
    run_large_scale_simulation(1000)