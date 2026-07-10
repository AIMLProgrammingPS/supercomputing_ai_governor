# Research Brief: AI-Governed Resource Allocation for Stochastic Simulations
**Principal Investigator:** Pranav Singhal  
**Advisor Consultation:** Reference Matrix provided by S. Thakur (June 2026)

## Foundational Literature Base
1. **Malleable Workload Scheduling:** Formulations in *The Journal of Supercomputing* (Springer) regarding performance-driven scheduling establish bounds for dynamically altering active runtimes.
2. **Dynamic HPC Cluster Management:** Implementations like DRAS-CQSim and Extensions of SLURM validate the use of Reinforcement Learning (RL) and state-action matrices for optimizing resource allocation under hardware constraints.

## Solution Architecture Definition
Our framework introduces a lightweight, low-overhead Python/NumPy execution environment optimized for resource-constrained client machines, bridging the gap between heavy HPC schedulers and accessible local deployment.

## Implementation Framework (July 2026 Status)
The codebase validates this architecture through three integrated components:
1. **Config-Driven Governor Agent (`GovernorAgent`)**: Dynamically parses target thresholds (e.g., CPU load limits, max queue capacity) with fault-tolerant exception handling.
2. **Mathematical Optimization Engine (`SimulationWorkloadGovernor`)**: Swaps execution strategies under load using a live `scipy.optimize.linprog` Linear Programming solver to maximize resource utility allocation.
3. **Telemetry & Visualization Matrix**: Outputs execution cycle performance tracking directly to structured CSV storage and compiles analytical graphs using `matplotlib`.