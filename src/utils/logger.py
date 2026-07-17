"""
The Journal of Supercomputing (Springer Nature)
Section: Artificial Intelligence
Track: Intelligent Resource Scheduling and Robust Optimization
Description: Simplified telemetry logger for tracking system performance 
             metrics and resource governor state changes.
"""

import time

def log_event(level: str, message: str):
    """Formats and prints simulation events with precise timestamps."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level.upper()}] {message}")

if __name__ == "__main__":
    log_event("info", "Telemetry logger initialized successfully.")