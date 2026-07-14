# Supercomputing AI Governor

An ultra-lightweight stochastic optimization and load mitigation framework designed to dynamically govern compute scaling metrics for high-fidelity Operations Research (OR) workloads on resource-constrained client endpoints.

## Target Submission Matrix

- **Journal:** *The Journal of Supercomputing* (Springer Nature)
- **Section:** Artificial Intelligence
- **Track:** Intelligent Resource Scheduling and Robust Optimization

---

# Core System Architecture

The ecosystem balances continuous simulation fidelity against host infrastructure constraints through three integrated modules:

1. **Config-Driven Governor Agent (`src/governor/agent.py`)**  
   A fault-tolerant runtime state classification wrapper that evaluates live CPU utilization registers and task queue backlogs against hyperparameter profiles.

2. **Robust Optimization Engine (`src/engine/resource_governor.py`)**  
   Formulates a polyhedrally constrained Robust Linear Programming (RLP) counterpart using a 4-variable decision matrix (`x₁`, `x₂`, `z₁`, `z₂`) solved via the HiGHS dual-simplex optimizer.

3. **Telemetry & Visualization Matrix (`src/utils/visualizer.py`)**  
   Compiles empirical phase distribution metrics across sequential execution horizons into structured CSV traces and comparative performance charts.

---

# Technical Performance Profile (N = 1000)

Stochastic evaluations performed on a multi-threaded benchmark suite (Monte Carlo asset pricing, PageRank vector power iterations, and capacitated Vehicle Routing algorithms) produced the following empirical results:

| Γ Value | Mean Load Reduction |
|---------:|-------------------:|
| **0.00** | **14.23%** |
| **0.25** | **15.94%** |
| **0.50** | **16.86%** |

---

# Installation

Install the required Python packages:

```bash
pip install numpy scipy pandas matplotlib
```

---

# Project Directory Creation

Before running any simulations, create the required output directories:

```bash
mkdir -p logs plots
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
Gamma 0.00: 14.23%
Gamma 0.25: 15.94%
Gamma 0.50: 16.86%
```