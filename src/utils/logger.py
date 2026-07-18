"""
The Journal of Supercomputing (Springer Nature)
Track: Simulation-Powered Innovation: Driving the Future of Digital Ecosystems
Description: Thread-safe telemetry logger tracking digital ecosystem state transitions.
"""

import time
import sys

def log_event(level: str, message: str):
    """Formats and prints simulation events with precise timestamps."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level.upper()}] {message}", flush=True)

if __name__ == "__main__":
    log_event("info", "Telemetry logger initialized successfully.")