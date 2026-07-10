"""
NUMTA 2026 Verification Suite
Description: Unit test validating that the SimulationWorkloadGovernor 
             correctly triggers resource throttling under high load.
"""

import unittest
from src.engine.resource_governor import SimulationWorkloadGovernor

class TestResourceGovernor(unittest.TestCase):
    def setUp(self):
        self.governor = SimulationWorkloadGovernor(available_cores=4, memory_bandwidth_gbps=16.0)

    def test_nominal_load_policy(self):
        # Under normal conditions, should run at full fidelity
        policy = self.governor.determine_execution_policy(current_cpu_load=50.0, total_pending_tasks=1000)
        self.assertEqual(policy["execution_mode"], "HIGH_FIDELITY_CONTINUOUS")
        self.assertEqual(policy["approximation_scale"], 1.0)

    def test_high_load_throttling_policy(self):
        # Under high load, should pivot to approximated discrete mode
        policy = self.governor.determine_execution_policy(current_cpu_load=90.0, total_pending_tasks=6000)
        self.assertEqual(policy["execution_mode"], "APPROXIMATED_DISCRETE_MILP")
        self.assertEqual(policy["approximation_scale"], 0.1)

if __name__ == "__main__":
    unittest.main()