"""
NUMTA 2026 Telemetry Plotting Engine
Description: Converts CSV telemetry output logs into clean, presentation-ready
             system optimization analytical graphs.
"""

import csv
import os
import matplotlib.pyplot as plt

def generate_performance_plots(csv_path: str = "logs/telemetry.csv", output_png: str = "logs/performance_chart.png"):
    if not os.path.exists(csv_path):
        print(f"[Visualizer Error] Cannot plot metrics. File {csv_path} does not exist.")
        return

    cycles, cpu_loads, tasks, modes = [], [], [], []
    
    with open(csv_path, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cycles.append(int(row["Cycle"]))
            cpu_loads.append(float(row["CPULoad"]))
            tasks.append(int(row["PendingTasks"]))
            modes.append(1 if row["Mode"] == "APPROXIMATED_DISCRETE_MILP" else 0)

    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Plot CPU load
    color = 'tab:red'
    ax1.set_xlabel('Simulation Execution Cycle')
    ax1.set_ylabel('CPU Utilization (%)', color=color)
    ax1.plot(cycles, cpu_loads, color=color, marker='o', linewidth=2, label="CPU Strain")
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Instantiate secondary axis for pending tasks
    ax2 = ax1.twinx()  
    color = 'tab:blue'
    ax2.set_ylabel('Pending Scheduler Queue Tasks', color=color)
    ax2.bar(cycles, tasks, color=color, alpha=0.3, width=0.4, label="Queue Tasks")
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('NUMTA 2026 AI Governor Optimization Vector Analysis', fontsize=14, pad=15)
    fig.tight_layout()
    
    os.makedirs(os.path.dirname(output_png), exist_ok=True)
    plt.savefig(output_png, dpi=300)
    print(f"[Visualizer Success] Analytical optimization performance graph saved to: {output_png}")

if __name__ == "__main__":
    generate_performance_plots()