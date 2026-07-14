# Supercomputing AI Governor

An ultra-lightweight stochastic optimization and load mitigation framework designed to dynamically govern compute scaling metrics for high-fidelity Operations Research (OR) workloads on resource-constrained client endpoints.

## Target Submission Matrix
* **Journal:** *The Journal of Supercomputing* (Springer Nature)
* **Section:** Artificial Intelligence
* **Track:** Intelligent Resource Scheduling and Robust Optimization

---

## Core System Architecture

The ecosystem balances continuous simulation fidelity against host infrastructure constraints through three integrated modules:

1. **Config-Driven Governor Agent (`src.governor.agent.py`)**: A fault-tolerant runtime state classification wrapper that evaluates live CPU utilization registers and task queue backlogs against hyperparameter profiles.
2. **Robust Optimization Engine (`src.engine.resource_governor.py`)**: Formulates a polyhedrally constrained Robust Linear Programming (RLP) Counterpart using a 4-variable decision matrix ($x_1, x_2, z_1, z_2$) solved via the high-performance HiGHS dual-simplex solver mechanics.
3. **Telemetry & Visualization Matrix (`src.utils.visualizer.py`)**: Compiles empirical phase distribution metrics across sequential execution horizons directly to structured CSV traces and outputs comparative performance charts.

---

## Technical Performance Profile (N=1000)

Stochastic evaluations run against a multi-threaded benchmark suite (Monte Carlo asset pricing, PageRank vector power iterations, and capacitive Vehicle Routing Algorithms) yield the following system distributions:

* **Baseline Operational Horizon ($\Gamma = 0.00$):** Eliminates system core-overheating flags entirely while generating an aggregate **14.74%** global load reduction.
* **Moderate Uncertainty Envelope ($\Gamma = 0.25$):** Scales physical safety margins to counteract telemetry noise, increasing the load shed efficiency factor to **16.51%**.
* **Conservative Robust Counterpart ($\Gamma = 0.50$):** Tightens the polyhedral boundary constraints to maximize endpoint stabilization, achieving an aggregate **17.46%** load reduction with sub-5ms thread latency constraints.

---

## Workflow Execution Command Matrix

All execution paths resolve imports absolute to the repository root via explicit path injection variables.

### 1. Verification Test Suite
Execute the internal unit verification assertions to validate optimization constraints:
```bash
export PYTHONPATH=. && python3 -m unittest discover -s tests
