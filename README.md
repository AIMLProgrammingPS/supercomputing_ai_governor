# Supercomputing AI Governor

An ultra-lightweight, native software middleware layer designed to dynamically govern compute scaling metrics for high-fidelity digital ecosystem modeling and Operations Research (OR) workloads on resource-constrained client endpoints.

## Target Submission Matrix

- **Journal:** *The Journal of Supercomputing* (Springer Nature)
- **Special Issue:** Simulation-Powered Innovation: Driving the Future of Digital Ecosystems
- **Track:** Advanced Paradigms and Software Architectures for Distributed and Real-Time Simulations

---

# Core System Architecture

The ecosystem balances continuous simulation fidelity against host infrastructure constraints through three integrated modules:

1. **Signal Conditioning Governor Agent (`src/governor/agent.py`)** A fault-tolerant runtime state classification wrapper that samples instantaneous CPU registers ($\hat{\rho}$) and scheduler backlogs ($\hat{Q}$). It passes raw telemetric input streams through a first-order recurrence Moving Average (EMA) filter to eradicate transient operating system noise and prevent controller chattering.

2. **Continuous Severity-Dependent Optimization Engine (`src/engine/resource_governor.py`)** Calculates a relative telemetric threshold overrun distance, or severity factor ($S_k \in [0, 1]$), the moment safety caps are breached. This factor dynamically modulates internal polyhedral bounds ($l_1(S_k), u_1(S_k)$) inside a 4-variable robust linear programming counterpart matrix resolved via the HiGHS dual-simplex solver engine.

3. **Telemetry & Visualization Matrix (`src/utils/visualizer.py`)** Compiles empirical across-run distribution metrics across sequential execution horizons into structured CSV traces, comparative validation charts, and cross-run statistical error bands.

---

# Technical Performance Profile (N = 30 Independent Multi-Seed Trajectories)

To isolate the optimization efficacy of our policy from frequency activation anomalies, the framework is validated under a strict **matched-signal ablation profile**. Both the robust governor and a conventional fixed-cap static baseline are subjected to identical EMA-filtered telemetry feeds. 

Cross-run metrics compiled across 30 independent stochastic simulation trajectories (Seeds 100–129) yield the following highly significant empirical profiles:

| Uncertainty Budget ($\Gamma$) | Static Baseline Mean Savings | Robust LP Governor Mean Savings | True Cross-Run 95% Confidence Range |
|:-----------------------------:|:----------------------------:|:-------------------------------:|:-----------------------------------:|
| **$\Gamma = 0.00$ (Nominal)** | 4.35%                        | **10.03%** | $[8.65\% \text{ -- } 11.42\%]$       |
| **$\Gamma = 0.25$ (Moderate)** | 4.35%                        | **10.54%** | $[9.09\% \text{ -- } 11.99\%]$       |
| **$\Gamma = 0.50$ (Severe)** | 4.35%                        | **10.14%** | $[8.75\% \text{ -- } 11.54\%]$       |

*Note: Tight variance bands across all parametric sweeps statistically confirm that the governor's architectural $2.4\times$ improvement over the baseline is structurally repeatable and completely isolated from localized sampling noise.*

---

# Installation

Install the required Python packages:

```bash
pip install numpy scipy pandas matplotlib---

# Project Directory Creation

Before running any simulations, create the required output directories:

```bash
mkdir -p logs
```

---

# Workflow Execution

## 1. Verification Execution (Micro-Horizon)

Runs a short simulation to verify logging and configuration.

```bash
export PYTHONPATH=. && python3 src/engine/simulation.py
```

---

## 2. High-Density Parametric Sweeps

Runs simulations across all Γ levels and generates telemetry CSV files.

```bash
export PYTHONPATH=. && python3 src/engine/scale_test.py
```

---

## 3. Analytics Visualization

Generates plots from the telemetry stored in the `logs/` directory.

```bash
export PYTHONPATH=. && python3 src/utils/visualizer.py
```

---

## 4. Regression Testing

Runs the complete unit test suite.

```bash
export PYTHONPATH=. && python3 -m unittest discover -s tests
```

---

## 5. Complete Pipeline Execution

Creates the required directories, regenerates telemetry, produces plots, and prints the empirical efficiency metrics.

```bash
mkdir -p logs plots && \
export PYTHONPATH=. && \
python3 src/engine/scale_test.py && \
python3 src/engine/simulation.py && \
python3 src/utils/visualizer.py && \
python3 -c "import pandas as pd; print(*(f'Gamma {g}: {pd.read_csv(f\"logs/scale_telemetry_gamma_{g:.2f}.csv\")[\"EfficiencySaved\"].mean()*100:.2f}%' for g in [0.00,0.25,0.50]), sep='\n')"
```

Expected output:

```
Gamma 0.00: 10.03%
Gamma 0.25: 10.54%
Gamma 0.50: 10.14%
```