"""
The Journal of Supercomputing (Springer Nature)
Track: Simulation-Powered Innovation: Driving the Future of Digital Ecosystems
Description: Unit testing framework establishing regression checks over governor state bounds.
"""

import unittest
from src.engine.resource_governor import SimulationWorkloadGovernor

class TestResourceGovernor(unittest.TestCase):
    def setUp(self):
        self.governor = SimulationWorkloadGovernor(available_cores=8, memory_bandwidth_gbps=32.0, gamma=0.25)

    def test_nominal_load_policy(self):
        """Validates that governor permits full-fidelity throughput during minimal stress."""
        self.governor.agent.reset_filter()
        policy = self.governor.determine_execution_policy(current_cpu_load=30.0, total_pending_tasks=400)
        self.assertEqual(policy["execution_mode"], "HIGH_FIDELITY_CONTINUOUS")
        self.assertEqual(policy["approximation_scale"], 1.0)

    def test_high_load_throttling_policy(self):
        """Validates that governor shifts safely to discrete solver mode under high sustained loads."""
        self.governor.agent.reset_filter()
        
        # Inject consecutive observations to surpass the EMA tracking threshold
        self.governor.determine_execution_policy(current_cpu_load=95.0, total_pending_tasks=7500)
        policy = self.governor.determine_execution_policy(current_cpu_load=98.0, total_pending_tasks=8000)
        
        self.assertEqual(policy["execution_mode"], "APPROXIMATED_DISCRETE_MILP")
        self.assertLess(policy["approximation_scale"], 1.0)
        self.assertGreaterEqual(policy["allocated_cores"], 1)

if __name__ == "__main__":
    unittest.main()