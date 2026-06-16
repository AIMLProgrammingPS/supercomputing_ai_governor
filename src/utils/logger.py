import os
import json
from datetime import datetime

class ResourceTelemetryLogger:
    def __init__(self, log_dir="logs", config_path="config/hyperparams.json"):
        self.log_dir = log_dir
        self.config_path = config_path
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, "hardware_performance.log")
        
        # Provision telemetry database structure
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                f.write("timestamp,batch_id,execution_time_sec,iterations_per_sec,memory_delta_mb,cache_status\n")
    def log_metrics(self, batch_id, exec_time, iterations, mem_delta, cache_status="STABLE"):
        """Logs localized hardware execution deltas for memory bus saturation analysis."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        throughput = iterations / exec_time if exec_time > 0 else 0
        log_line = f"{timestamp},{batch_id},{exec_time:.6f},{throughput:.2f},{mem_delta:.4f},{cache_status}\n"
        
        with open(self.log_file, "a") as f:
            f.write(log_line)
                    
        print(f"[TELEMETRY] Batch {batch_id} | Throughput: {throughput:.2f} iter/sec | Mem Delta: {mem_delta:.2f}MB")
    def load_threshold_configs(self):
        """Dynamic look-up for hardware threshold limits from the config layer."""
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"max_memory_threshold_mb": 512, "target_latency_ms": 15.0}