"""
The Journal of Supercomputing (Springer Nature)
Section: Artificial Intelligence
Track: Intelligent Resource Scheduling and Robust Optimization
Description: Mass-scale stochastic simulation engine (1,000+ cycles) 
             evaluating Robust LP Counterparts across varying uncertainty budgets.
"""

import csv
import os
import random
from src.engine.resource_governor import SimulationWorkloadGovernor
from src.utils.logger import log_event

def run_large_scale_simulation(total_cycles: int = 1000, gamma: float = 0.00):
    governor = SimulationWorkloadGovernor(available_cores=8, memory_bandwidth_gbps=32.0, gamma=gamma)
    log_event("info", f"Initializing robust high-density simulation matrix: {total_cycles} cycles at Gamma={gamma}...")
    
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    csv_path = os.path.join(log_dir, f"scale_telemetry_gamma_{gamma:.2f}.csv")
    
    milp_count = 0
    high_fid_count = 0
    cumulative_efficiency_saved = 0.0
    
    # Reset random seed to ensure identical system strain vectors across different Gamma evaluations
    random.seed(42)
    
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Cycle", "CPULoad", "PendingTasks", "Mode", "EfficiencySaved"])
        
        for cycle in range(1, total_cycles + 1):
            # Generate stochastic system strain vectors based on Research Brief bounds
            simulated_cpu_load = random.uniform(40.0, 98.0)
            simulated_pending_tasks = random.randint(800, 8000)
            
            policy = governor.determine_execution_policy(
                current_cpu_load=simulated_cpu_load,
                total_pending_tasks=simulated_pending_tasks
            )
            
            if policy["execution_mode"] == "APPROXIMATED_DISCRETE_MILP":
                milp_count += 1
                # Gained efficiency = (1.0 - memory bandwidth scaling factor) * optimization efficiency metric
                saved_overhead = (1.0 - policy["approximation_scale"]) * policy["optimized_efficiency"]
            else:
                high_fid_count += 1
                saved_overhead = 0.0
                
            cumulative_efficiency_saved += saved_overhead
            
            writer.writerow([
                cycle, round(simulated_cpu_load, 2), simulated_pending_tasks, 
                policy["execution_mode"], round(saved_overhead, 4)
            ])
            
            if cycle % 200 == 0:
                log_event("info", f"[Gamma={gamma:.2f}] Completed {cycle}/{total_cycles} cycles...")

    milp_ratio = (milp_count / total_cycles) * 100
    avg_efficiency = (cumulative_efficiency_saved / total_cycles) * 100
    
    print("\n" + "="*60)
    print(f"    JOURNAL OF SUPERCOMPUTING EVALUATION METRICS (Gamma = {gamma:.2f})")
    print("="*60)
    print(f"Total Simulated Operational Cycles    : {total_cycles}")
    print(f"High-Fidelity Baseline Windows        : {high_fid_count} ({100 - milp_ratio:.1f}%)")
    print(f"Active Robust LP Mitigations Triggered: {milp_count} ({milp_ratio:.1f}%)")
    print(f"Aggregate Infrastructure Load Saved   : {avg_efficiency:.2f}% reduction")
    print("="*60 + "\n")

if __name__ == "__main__":
    # Parametric sweep across polyhedral uncertainty horizons
    for gamma_val in [0.00, 0.25, 0.50]:
        run_large_scale_simulation(total_cycles=1000, gamma=gamma_val)