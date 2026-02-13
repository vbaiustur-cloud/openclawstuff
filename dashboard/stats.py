#!/usr/bin/env python3
"""
Usage statistics for OpenClaw
Tracks: Token usage, cron success/failure, health scores
"""

import json
import os
from datetime import datetime
from pathlib import Path

STATS_DIR = Path.home() / ".openclaw" / "stats"
STATS_FILE = STATS_DIR / "usage.json"

class UsageStats:
    def __init__(self):
        STATS_DIR.mkdir(parents=True, exist_ok=True)
        if not STATS_FILE.exists():
            self.data = self._init_data()
            self.save()
        else:
            self.load()
    
    def _init_data(self):
        return {
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "models": {},
            "crons": {
                "total_runs": 0,
                "successes": 0,
                "failures": 0,
                "by_job": {}
            },
            "health_scores": []
        }
    
    def load(self):
        with open(STATS_FILE) as f:
            self.data = json.load(f)
    
    def save(self):
        self.data["last_updated"] = datetime.now().isoformat()
        with open(STATS_FILE, "w") as f:
            json.dump(self.data, f, indent=2, default=str)
    
    def log_model_usage(self, model: str, prompt_tokens: int, completion_tokens: int):
        if model not in self.data["models"]:
            self.data["models"][model] = {
                "requests": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "first_used": datetime.now().isoformat(),
                "last_used": datetime.now().isoformat()
            }
        
        self.data["models"][model]["requests"] += 1
        self.data["models"][model]["prompt_tokens"] += prompt_tokens
        self.data["models"][model]["completion_tokens"] += completion_tokens
        self.data["models"][model]["total_tokens"] += prompt_tokens + completion_tokens
        self.data["models"][model]["last_used"] = datetime.now().isoformat()
        self.save()
    
    def log_cron_run(self, job_name: str, success: bool, duration_ms: int = 0):
        self.data["crons"]["total_runs"] += 1
        if success:
            self.data["crons"]["successes"] += 1
        else:
            self.data["crons"]["failures"] += 1
        
        if job_name not in self.data["crons"]["by_job"]:
            self.data["crons"]["by_job"][job_name] = {
                "total_runs": 0,
                "successes": 0,
                "failures": 0,
                "avg_duration_ms": 0
            }
        
        job = self.data["crons"]["by_job"][job_name]
        job["total_runs"] += 1
        if success:
            job["successes"] += 1
        else:
            job["failures"] += 1
        
        if duration_ms > 0:
            job["avg_duration_ms"] = int((job["avg_duration_ms"] * (job["total_runs"] - 1) + duration_ms) / job["total_runs"])
        
        self.save()
    
    def log_health_score(self, score: float, details: dict = None):
        self.data["health_scores"].append({
            "timestamp": datetime.now().isoformat(),
            "score": score,
            "details": details or {}
        })
        self.data["health_scores"] = self.data["health_scores"][-100:]
        self.save()
    
    def get_summary(self) -> dict:
        """Get usage summary"""
        crons = self.data["crons"]
        success_rate = (crons["successes"] / crons["total_runs"] * 100) if crons["total_runs"] > 0 else 0
        
        avg_health = 0
        if self.data["health_scores"]:
            scores = [s["score"] for s in self.data["health_scores"]]
            avg_health = sum(scores) / len(scores)
        
        return {
            "models": self.data["models"],
            "crons": {
                "total_runs": crons["total_runs"],
                "successes": crons["successes"],
                "failures": crons["failures"],
                "success_rate": f"{success_rate:.1f}%",
                "by_job": crons["by_job"]
            },
            "health": {
                "average_score": f"{avg_health:.1f}",
                "recent_checks": len(self.data["health_scores"])
            }
        }
    
    def display(self):
        """Display stats in terminal-friendly format"""
        summary = self.get_summary()
        
        print("\n" + "="*60)
        print("OPENCLAW USAGE STATISTICS")
        print("="*60)
        print(f"Last Updated: {self.data['last_updated']}")
        
        print("\n### Model Usage")
        if summary["models"]:
            print(f"{'Model':<30} {'Requests':<10} {'Prompt Tokens':<15} {'Completion':<12} {'Total':<10}")
            print("-" * 77)
            for model, stats in summary["models"].items():
                print(f"{model:<30} {stats['requests']:<10} {stats['prompt_tokens']:<15} {stats['completion_tokens']:<12} {stats['total_tokens']:<10}")
        else:
            print("No model usage recorded yet.")
        
        print("\n### Cron Jobs")
        crons = summary["crons"]
        print(f"Total Runs: {crons['total_runs']}")
        print(f"Successes:  {crons['successes']}")
        print(f"Failures:   {crons['failures']}")
        print(f"Success Rate: {crons['success_rate']}")
        
        if crons["by_job"]:
            print(f"\n{'Job Name':<25} {'Runs':<8} {'Success':<8} {'Fail':<8} {'Avg Duration':<15}")
            print("-" * 70)
            for job, stats in crons["by_job"].items():
                print(f"{job:<25} {stats['total_runs']:<8} {stats['successes']:<8} {stats['failures']:<8} {stats['avg_duration_ms']:<15}ms")
        
        print("\n### Health Scores")
        health = summary["health"]
        print(f"Average Score: {health['average_score']}/100")
        print(f"Recent Checks: {health['recent_checks']}")
        
        print("\n" + "="*60)

def main():
    stats = UsageStats()
    stats.display()

if __name__ == "__main__":
    main()
