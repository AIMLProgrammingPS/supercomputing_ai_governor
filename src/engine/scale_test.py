"""
The Journal of Supercomputing (Springer Nature)
Track: Simulation-Powered Innovation: Driving the Future of Digital Ecosystems
Description: High-density verification suite executing true multi-seed comparative baselines 
             (No Governor vs. Matched-Signal Static Cap vs. Robust Governor) calculating across-run 95% CIs.
"""

import csv
import os
import random
import numpy as np
import scipy.stats as st
from src.engine.resource_governor import SimulationWorkloadGovernor
from src.utils.logger import log_event

def run_multi_seed_evaluation(total_seeds: int = 30, execution_cycles: int = 100, gamma: float = 0.00):
    log_event("info", f"Starting multi-seed evaluation ({total_seeds} runs) for Gamma = {gamma:.2f} against matched baselines...")
    
    governor_savings_across_seeds = []
    static_savings_across_seeds = []
    
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    csv_path = os.path.join(log_dir, f"scale_telemetry_gamma_{gamma:.2f}.csv")
    
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Seed", "Cycle", "RawCPU", "Tasks", "GovMode", "GovSaved", "StaticSaved"])
        
        for run_seed in range(100, 100 + total_seeds):
            random.seed(run_seed)
            governor = SimulationWorkloadGovernor(available_cores=8, memory_bandwidth_gbps=32.0, gamma=gamma)
            governor.agent.reset_filter()
            
            gov_saved_run_accumulator = 0.0
            static_saved_run_accumulator = 0.0
            
            for cycle in range(1, execution_cycles + 1):
                raw_cpu = random.uniform(45.0, 98.0)
                pending_tasks = random.randint(500, 8000)
                
                # 1. Evaluate Robust LP Governor Policy (This handles internal EMA smoothing)
                gov_policy = governor.determine_execution_policy(raw_cpu, pending_tasks)
                
                # Extract the smoothed metrics calculated inside the governor agent
                smooth_cpu = gov_policy["smoothed_cpu"]
                smooth_task = gov_policy["smoothed_task"]
                
                if gov_policy["execution_mode"] == "APPROXIMATED_DISCRETE_MILP":
                    gov_saved = (1.0 - gov_policy["approximation_scale"]) * gov_policy["optimized_efficiency"]
                else:
                    gov_saved = 0.0
                
                # 2. MATCHED-SIGNAL BASELINE: Evaluates the EXACT same smoothed values to eliminate frequency bias
                if smooth_cpu > governor.agent.cpu_threshold or smooth_task > governor.agent.task_threshold:
                    static_saved = 0.50 * 0.40  # Static reduction ratio * expected performance loss
                else:
                    static_saved = 0.0
                    
                gov_saved_run_accumulator += gov_saved
                static_saved_run_accumulator += static_saved
                
                writer.writerow([
                    run_seed, cycle, round(raw_cpu, 2), pending_tasks,
                    gov_policy["execution_mode"], round(gov_saved, 4), round(static_saved, 4)
                ])
            
            governor_savings_across_seeds.append((gov_saved_run_accumulator / execution_cycles) * 100)
            static_savings_across_seeds.append((static_saved_run_accumulator / execution_cycles) * 100)

    # Statistical Evaluation Engine: Compute 95% CI correctly across unique run distributions
    def calculate_cross_run_confidence(data):
        n = len(data)
        mean = np.mean(data)
        sem = st.sem(data)
        if sem == 0:
            return mean, 0.0, 0.0
        interval = sem * st.t.ppf((1 + 0.95) / 2., n - 1)
        return mean, mean - interval, mean + interval

    gov_mean, gov_low, gov_high = calculate_cross_run_confidence(governor_savings_across_seeds)
    stat_mean, _, _ = calculate_cross_run_confidence(static_savings_across_seeds)
    
    print("\n" + "="*65)
    print(f"   VALIDATED MULTI-SEED METRICS PROFILE (Gamma = {gamma:.2f})")
    print("="*65)
    print(f"Evaluated Independent Seeds         : {total_seeds}")
    print(f"Static Baseline Mean Savings        : {stat_mean:.2f}%")
    print(f"Robust LP Governor Mean Savings     : {gov_mean:.2f}%")
    print(f"True Cross-Run 95% Confidence Range : [{gov_low:.2f}% - {gov_high:.2f}%]")
    print("="*65 + "\n")
    
    return gov_mean

if __name__ == "__main__":
    for uncertainty_budget in [0.00, 0.25, 0.50]:
        run_multi_seed_evaluation(total_seeds=30, execution_cycles=100, gamma=uncertainty_budget)