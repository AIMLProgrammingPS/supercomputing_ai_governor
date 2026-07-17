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
            simulated_cpu_load = random.uniform(40.0, 98.0)
            simulated_pending_tasks = random.randint(800, 8000)
            
            policy = governor.determine_execution_policy(
                current_cpu_load=simulated_cpu_load, 
                total_pending_tasks=simulated_pending_tasks
            )
            
            # The baseline configuration uses: (1.0 - policy["approximation_scale"]) * policy["optimized_efficiency"]
            # Under APPROXIMATED_DISCRETE_MILP: (1.0 - 0.7) * optimized_efficiency = 0.3 * optimized_efficiency
            if policy["execution_mode"] == "APPROXIMATED_DISCRETE_MILP":
                milp_count += 1
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

    # Compute empirical metrics dynamically from the live tracking metrics loop
    display_high_fid = high_fid_count
    display_milp = milp_count
    display_eff = (cumulative_efficiency_saved / total_cycles) * 100

    milp_ratio = (display_milp / total_cycles) * 100
    high_fid_ratio = (display_high_fid / total_cycles) * 100
    
    print("\n" + "="*60)
    print(f"    JOURNAL OF SUPERCOMPUTING EVALUATION METRICS (Gamma = {gamma:.2f})")
    print("="*60)
    print(f"Total Simulated Operational Cycles    : {total_cycles}")
    print(f"High-Fidelity Baseline Windows        : {display_high_fid} ({high_fid_ratio:.1f}%)")
    print(f"Active Robust LP Mitigations Triggered: {display_milp} ({milp_ratio:.1f}%)")
    print(f"Aggregate Infrastructure Load Saved   : {display_eff:.2f}% reduction")
    print("="*60 + "\n")

if __name__ == "__main__":
    for uncertainty_budget in [0.00, 0.25, 0.50]:
        run_large_scale_simulation(total_cycles=1000, gamma=uncertainty_budget)