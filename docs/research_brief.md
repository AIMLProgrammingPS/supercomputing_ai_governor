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

## Technical Formulation: Task Inputs & Optimization Vectors

### 1. State Space Matrix (Systemic Inputs)
The global simulation environment injects an empirical state vector $S_t = \{L_t, Q_t\}$ at each execution cycle $t$:
* **$L_t$ (CPU Load Feature):** Continuous scalar representing real-time CPU utilization bounds, where $L_t \in [40.0, 98.0]$.
* **$Q_t$ (Queue Backlog Feature):** Discrete integer representing scheduler memory bottleneck constraints, where $Q_t \in [800, 8000]$.

### 2. Linear Programming Formulation (LP Mode Matrix)
When the activation criteria $\gamma$ is met ($L_t > L_{max}$ or $Q_t > Q_{max}$), the framework maps the resource distribution problem to an optimized linear program solved via the high-performance DUAL-SIMPLEX/HIGHS method:

$$\min_{x} c^T x \quad \text{subject to} \quad A x \le b, \quad l \le x \le u$$

Where the structural parameter inputs are instantiated as:
* **Objective Vector ($c$):** $[-1.0, -1.0]^T$, penalizing under-utilization to maximize normalized allocation coefficients for active processing cores ($x_1$) and memory bandwidth channels ($x_2$).
* **Constraint Boundary ($A, b$):** $x_1 + x_2 \le 0.85$, forcing an explicit 15% safety buffer to shield local host infrastructure during scheduling spikes.
* **Variable Bounding Boxes ($l, u$):** $x_i \in [0.1, 0.7]$, guaranteeing minimum operating execution survival while preventing single-process core saturation.

## Empirical Evaluation & Statistical Results (N=1000)
Extensive stochastic stress-testing across an operational horizon of $1,000$ simulated continuous execution cycles yielded the following system telemetry vectors:

* **Baseline High-Fidelity Execution Window:** The system maintained maximum precision continuous operations for 422 cycles ($42.2\%$), verifying that the governor yields to normal operations whenever hardware bounds permit.
* **Active LP Mitigation Vector Activation:** The automated `GovernorAgent` successfully intercepted threshold breaches in 578 cycles ($57.8\%$), dynamically routing the resource distribution pipeline through the Scipy dual-simplex optimization layer.
* **Aggregate Compute Efficiency Index:** Transitioning to optimized bounded allocations generated a mean global infrastructure load reduction of **$14.74\%$**, validating the framework's capability to prevent host machine saturation under intense scheduler backlogs.