import csv
import os
import logging
from datetime import datetime

logger = logging.getLogger("ResultManager")

class ResultManager:
    def __init__(self, filename="test_results.csv"):
        self.filepath = os.path.join(os.path.dirname(__file__), filename)
        self.results = []
        self.headers = ["id", "test_name", "status", "tools_called", "query", "error", "timestamp"]

    def add_result(self, turn_id, test_name, query, status, tools, error=""):
        self.results.append({
            "id": turn_id,
            "test_name": test_name,
            "query": query,
            "status": status,
            "tools_called": ", ".join(tools) if tools else "None",
            "error": error,
            "timestamp": datetime.now().isoformat()
        })

    def save(self):
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(self.results)
        logger.info(f"Results saved to {self.filepath}")
