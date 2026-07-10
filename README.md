# Supercomputing AI Governor

An AI-driven execution framework built at the intersection of Operations Research (OR) and Machine Learning to dynamically adapt heavy simulation computational scaling based on real-time hardware resource availability.

## NUMTA 2026 Target Tracks
- **Resource Allocation and Scheduling**
- **Numerical Simulation in OR**
- **Parallel and Distributed Computing in OR**
- **Artificial Intelligence / Machine Learning in OR**

## Core Architecture
1. **`GovernorAgent`**: Dynamic configuration loader that evaluates system state and thresholds.
2. **`SimulationWorkloadGovernor`**: Decoupled resource manager that sets approximation scaling rules.
3. **`Simulation Loop`**: High-performance discrete-event workload execution harness.

## Quickstart
```bash
# Run the verification test suite
python3 -m unittest tests/test_engine.py

# Launch the live adaptive simulation
python3 -m src.engine.simulation