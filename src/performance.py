from typing import List


class PerformanceMonitor:
    """Monitor and analyze workflow performance"""

    def __init__(self):
        self.runs = []
        self.step_metrics = {}

    def record_run(self, state: dict):
        """Record metrics from a completed workflow run"""
        run_data = {
            "query": state.get("query", ""),
            "execution_time": state.get("execution_time", 0),
            "step_count": state.get("step_count", 0),
            "token_estimate": state.get("token_estimate", 0),
            "cost_estimate": state.get("cost_estimate", 0),
            "has_error": state.get("error") is not None,
            "steps": state.get("trace_metadata", {}).get("steps", [])
        }

        self.runs.append(run_data)

        # Aggregate step-level metrics
        for step in run_data["steps"]:
            step_name = step.get("step_name", "unknown")
            if step_name not in self.step_metrics:
                self.step_metrics[step_name] = {
                    "durations": [],
                    "tokens": [],
                    "costs": [],
                    "success_count": 0,
                    "failure_count": 0
                }

            self.step_metrics[step_name]["durations"].append(step.get("duration", 0))
            self.step_metrics[step_name]["tokens"].append(step.get("tokens", 0))
            self.step_metrics[step_name]["costs"].append(step.get("cost", 0))

            if step.get("status") == "success":
                self.step_metrics[step_name]["success_count"] += 1
            else:
                self.step_metrics[step_name]["failure_count"] += 1

    def get_summary(self) -> dict:
        """Get performance summary"""
        if not self.runs:
            return {"total_runs": 0, "message": "No runs recorded"}

        total_time = sum(r["execution_time"] for r in self.runs)
        total_tokens = sum(r["token_estimate"] for r in self.runs)
        total_cost = sum(r["cost_estimate"] for r in self.runs)
        error_count = sum(1 for r in self.runs if r["has_error"])

        return {
            "total_runs": len(self.runs),
            "avg_execution_time": total_time / len(self.runs),
            "total_tokens": total_tokens,
            "avg_tokens_per_run": total_tokens / len(self.runs),
            "total_cost": total_cost,
            "avg_cost_per_run": total_cost / len(self.runs),
            "error_rate": error_count / len(self.runs)
        }

    def get_step_analysis(self) -> dict:
        """Get per-step performance analysis"""
        analysis = {}

        for step_name, metrics in self.step_metrics.items():
            durations = metrics["durations"]
            tokens = metrics["tokens"]
            total_runs = metrics["success_count"] + metrics["failure_count"]

            if durations and total_runs > 0:
                analysis[step_name] = {
                    "avg_duration": sum(durations) / len(durations),
                    "max_duration": max(durations),
                    "min_duration": min(durations),
                    "avg_tokens": sum(tokens) / len(tokens) if tokens else 0,
                    "success_rate": metrics["success_count"] / total_runs
                }

        return analysis

    def get_recommendations(self) -> List[dict]:
        """Generate optimization recommendations"""
        recommendations = []
        step_analysis = self.get_step_analysis()

        for step_name, metrics in step_analysis.items():
            if metrics["avg_duration"] > 5.0:
                recommendations.append({
                    "step": step_name,
                    "issue": "High latency",
                    "metric": "{:.2f}s average".format(metrics['avg_duration']),
                    "suggestion": "Consider using a faster model or shorter prompts"
                })

            if metrics["avg_tokens"] > 1000:
                recommendations.append({
                    "step": step_name,
                    "issue": "High token usage",
                    "metric": "{:.0f} average tokens".format(metrics['avg_tokens']),
                    "suggestion": "Reduce prompt length or implement chunking"
                })

            if metrics["success_rate"] < 0.95:
                recommendations.append({
                    "step": step_name,
                    "issue": "Low success rate",
                    "metric": "{:.1%}".format(metrics['success_rate']),
                    "suggestion": "Add retry logic or improve error handling"
                })

        return recommendations

    def print_report(self):
        """Print a formatted performance report"""
        print("\n" + "=" * 50)
        print("📊 PERFORMANCE REPORT")
        print("=" * 50)

        summary = self.get_summary()
        print("\nOverall Metrics:")
        print("  Total runs: {}".format(summary.get('total_runs', 0)))
        print("  Avg execution time: {:.2f}s".format(
            summary.get('avg_execution_time', 0)))
        print("  Avg tokens/run: {:.0f}".format(
            summary.get('avg_tokens_per_run', 0)))
        print("  Avg cost/run: ${:.6f}".format(
            summary.get('avg_cost_per_run', 0)))
        print("  Error rate: {:.1%}".format(summary.get('error_rate', 0)))

        step_analysis = self.get_step_analysis()
        if step_analysis:
            print("\nPer-Step Analysis:")
            for step_name, metrics in step_analysis.items():
                print("\n  {}:".format(step_name.upper()))
                print("    Avg duration: {:.2f}s".format(metrics['avg_duration']))
                print("    Avg tokens: {:.0f}".format(metrics['avg_tokens']))
                print("    Success rate: {:.1%}".format(metrics['success_rate']))

        recommendations = self.get_recommendations()
        if recommendations:
            print("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                print("  {}. {}: {}".format(i, rec['step'], rec['issue']))
                print("     Suggestion: {}".format(rec['suggestion']))
