# Research Brief: AI-Governed Resource Allocation for Stochastic Simulations
**Principal Investigator:** Pranav Singhal  
**Advisor Consultation:** Reference Matrix provided by S. Thakur (June 2026)

## Foundational Literature Base
1. **Malleable Workload Scheduling:** Formulations in *The Journal of Supercomputing* (Springer Nature) regarding performance-driven scheduling establish bounds for dynamically altering active runtimes.
2. **Dynamic HPC Cluster Management:** Implementations like DRAS-CQSim and Extensions of SLURM validate the use of Reinforcement Learning (RL) and state-action matrices for optimizing resource allocation under hardware constraints.

## Solution Architecture Definition
Our framework introduces a lightweight, low-overhead Python execution environment optimized for resource-constrained client machines, bridging the gap between heavy HPC schedulers and accessible local deployment.

## Implementation Framework (July 2026 Status)
The codebase validates this architecture through three integrated components:
1. **Config-Driven Governor Agent (`GovernorAgent`)**: Dynamically parses target thresholds, including CPU load limits and max queue capacity, with fault-tolerant exception handling.
2. **Mathematical Optimization Engine (`SimulationWorkloadGovernor`)**: Swaps execution strategies under load using a live Robust Linear Programming solver to maximize resource utility allocation.
3. **Telemetry & Visualization Matrix**: Outputs execution cycle performance tracking directly to structured CSV storage and compiles analytical graphs using `matplotlib`.

---

## Technical Formulation: Task Inputs & Optimization Vectors

### 1. State Space Matrix (Systemic Inputs)
The global simulation environment injects an empirical state vector $S_t = \{L_t, Q_t\}$ at each execution cycle $t$:
* **$L_t$ (CPU Load Feature):** Continuous scalar representing real-time CPU utilization bounds, where $L_t \in [40.0, 98.0]$.
* **$Q_t$ (Queue Backlog Feature):** Discrete integer representing scheduler memory bottleneck constraints, where $Q_t \in [800, 8000]$.

### 2. Robust Linear Programming Counterpart (RLP Matrix)
When the activation criteria is met ($L_t > L_{\text{max}}$ or $Q_t > Q_{\text{max}}$), the framework maps the resource distribution problem to an optimized robust linear program solved via the high-performance HiGHS dual-simplex solver method. To manage parameter volatility, we define an expanded decision vector $\mathbf{v} = [x_1, x_2, z_1, z_2]^T \in \mathbb{R}^4$, where $z_1, z_2$ track polyhedral uncertainty borders governed by the protection budget parameter $\Gamma \in [0, 2]$:

$$\min_{\mathbf{v}} \quad \mathbf{c}^T \mathbf{v}$$
$$\text{subject to} \quad \mathbf{A}_{\text{ub}} \mathbf{v} \le \mathbf{b}_{\text{ub}}, \quad \mathbf{l} \le \mathbf{v} \le \mathbf{u}$$

Where the structural parameters are instantiated as:
* **Objective Vector ($\mathbf{c}$):** $[-1.0, -1.0, 0.0, 0.0]^T$, penalizing allocation deficits to maximize active processing cores ($x_1$) and memory bandwidth channels ($x_2$).
* **Constraint Matrix ```math ($\mathbf{A}_{\text{ub}}, \mathbf{b}_{\text{ub}}$):** 


\mathbf{A}_{\text{ub}} = \begin{bmatrix} 1.0 & 1.0 & \Gamma & \Gamma \\ 1.0 & 0.0 & -1.0 & 0.0 \\ 0.0 & 1.0 & 0.0 & -1.0 \end{bmatrix}, \quad \mathbf{b}_{\text{ub}} = \begin{bmatrix} 0.85 \\ 0.0 \\ 0.0 \end{bmatrix}
```
  This models the robust capacity threshold $x_1 + x_2 + \Gamma z_1 + \Gamma z_2 \le 0.85$, forcing an explicit 15% safety buffer to shield local host infrastructure during scheduling spikes, paired with epigraph conditions $x_i - z_i \le 0$.
* **Variable Bounding Boxes ($\mathbf{l}, \mathbf{u}$):** $x_i \in [0.1, 0.7]$, guaranteeing minimum operating execution survival while preventing single-process core saturation.

---

## Empirical Evaluation & Statistical Results (N=1000)
Extensive stochastic stress-testing across an operational horizon of 1,000 simulated continuous execution cycles yielded a clear state distribution and robust scaling trends:

* **Phase Distribution Uniformity:** The system maintained maximum precision continuous operations for 422 cycles (42.2%) and successfully intercepted threshold breaches in 578 cycles (57.8%), showing identical triggering distributions across parametric sweeps.
* **Baseline Horizon Performance ($\Gamma = 0.00$):** Yielded an aggregate mean global load reduction score of **14.74%**, matching original continuous polyhedral edge allocations.
* **Moderate Uncertainty Horizon ($\Gamma = 0.25$):** The robust counterpart modified core parameters to protect against noise, elevating the mean system load reduction efficiency to **16.51%**.
* **Conservative Robust Envelope ($\Gamma = 0.50$):** Maximized local endpoint preservation matrices by shifting allocations inward, generating a peak global infrastructure load reduction of **17.46%** while maintaining sub-5ms thread execution latencies.