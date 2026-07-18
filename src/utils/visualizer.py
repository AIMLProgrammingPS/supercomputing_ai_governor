"""
The Journal of Supercomputing (Springer Nature)
Track: Simulation-Powered Innovation: Driving the Future of Digital Ecosystems
Description: Compiles and exports publication-grade performance profile charts.
"""

import os
import csv
import matplotlib.pyplot as plt

def generate_performance_plots(csv_path: str = "logs/telemetry.csv", output_png: str = "logs/performance_chart.png"):
    if not os.path.exists(csv_path):
        print(f"[Visualizer Error] Cannot trace data. Target {csv_path} does not exist.")
        return

    cycles, cpu_loads, tasks = [], [], []
    
    with open(csv_path, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cycles.append(int(row["Cycle"]))
            cpu_loads.append(float(row["CPULoad"]))
            tasks.append(int(row["PendingTasks"]))

    fig, ax1 = plt.subplots(figsize=(9, 5))

    color = '#d62728'
    ax1.set_xlabel('Simulation Execution Cycle', fontweight='bold')
    ax1.set_ylabel('CPU Utilization (%)', color=color, fontweight='bold')
    ax1.plot(cycles, cpu_loads, color=color, marker='o', linewidth=2, label="Measured CPU Load")
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, linestyle='--', alpha=0.5)

    ax2 = ax1.twinx()  
    color = '#1f77b4'
    ax2.set_ylabel('Pending Scheduler Queue Tasks', color=color, fontweight='bold')
    ax2.bar(cycles, tasks, color=color, alpha=0.25, width=0.4, label="Queue Load Balance")
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Ecosystem Governance Metrics (Simulation-Powered Innovation)', fontsize=11, fontweight='bold')
    fig.tight_layout()
    
    os.makedirs(os.path.dirname(output_png) or '.', exist_ok=True)
    plt.savefig(output_png, dpi=300)
    plt.close()
    print(f"[Visualizer Success] Publication chart created successfully at: {output_png}")

if __name__ == "__main__":
    generate_performance_plots()