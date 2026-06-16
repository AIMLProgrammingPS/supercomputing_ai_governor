import os
import json
from datetime import datetime

class ResourceTelemetryLogger:
    def __init__(self, log_dir="logs", config_path="config/hyperparams.json"):
        self.log_dir = log_dir
        self.config_path = config_path
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, "hardware_performance.log")