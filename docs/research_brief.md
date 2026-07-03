# Research Brief: AI-Governed Resource Allocation for Stochastic Simulations
**Principal Investigator:** Pranav Singhal  
**Advisor Consultation:** Reference Matrix provided by S. Thakur (June 2026)

## Foundational Literature Base
1. **Malleable Workload Scheduling:** Formulations in *The Journal of Supercomputing* (Springer) regarding performance-driven scheduling establish bounds for dynamically altering active runtimes.
2. **Dynamic HPC Cluster Management:** Implementations like DRAS-CQSim and Extensions of SLURM validate the use of Reinforcement Learning (RL) and state-action matrices for optimizing resource allocation under hardware constraints.

## Solution Architecture Definition
Our framework introduces a lightweight, low-overhead Python/NumPy execution environment optimized for resource-constrained client machines, bridging the gap between heavy HPC schedulers and accessible local deployment.
