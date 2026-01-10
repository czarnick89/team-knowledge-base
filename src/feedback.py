import time
from typing import List


class FeedbackCollector:
    """Collect and analyze user feedback"""

    def __init__(self):
        self.feedback_entries = []

    def submit_feedback(self, trace_id: str, score: int,
                        comment: str = "", tags: List[str] = None):
        """Submit feedback for a trace"""
        if not 1 <= score <= 5:
            raise ValueError("Score must be between 1 and 5")

        entry = {
            "trace_id": trace_id,
            "timestamp": time.time(),
            "score": score,
            "comment": comment,
            "tags": tags or []
        }

        self.feedback_entries.append(entry)
        return entry

    def get_summary(self) -> dict:
        """Get feedback summary"""
        if not self.feedback_entries:
            return {"total_feedback": 0, "message": "No feedback recorded"}

        scores = [f["score"] for f in self.feedback_entries]

        return {
            "total_feedback": len(self.feedback_entries),
            "avg_score": sum(scores) / len(scores),
            "score_distribution": {
                i: scores.count(i) for i in range(1, 6)
            },
            "positive_rate": sum(1 for s in scores if s >= 4) / len(scores),
            "negative_rate": sum(1 for s in scores if s <= 2) / len(scores)
        }

    def get_insights(self) -> List[str]:
        """Generate insights from feedback"""
        insights = []
        summary = self.get_summary()

        if summary.get("total_feedback", 0) == 0:
            return ["Not enough feedback to generate insights"]

        avg = summary["avg_score"]
        pos_rate = summary["positive_rate"]
        neg_rate = summary["negative_rate"]

        if avg >= 4.0:
            insights.append(f"High satisfaction: {avg:.1f}/5 average score")
        elif avg <= 2.5:
            msg = f"Low satisfaction: {avg:.1f}/5 average score - needs attention"
            insights.append(msg)
        else:
            insights.append(f"Moderate satisfaction: {avg:.1f}/5 average score")

        if pos_rate >= 0.7:
            insights.append(f"{pos_rate:.0%} of responses rated positively (4-5 stars)")

        if neg_rate >= 0.2:
            insights.append(f"{neg_rate:.0%} of responses rated negatively (1-2 stars)")

        comments = [f["comment"] for f in self.feedback_entries if f["comment"]]
        if comments:
            insights.append(f"{len(comments)} feedback entries include comments")

        return insights

    def print_report(self):
        """Print feedback report"""
        print("\n" + "=" * 50)
        print("📝 FEEDBACK REPORT")
        print("=" * 50)

        summary = self.get_summary()

        if summary.get("total_feedback", 0) == 0:
            print("\nNo feedback recorded yet")
            return

        print(f"\nTotal feedback entries: {summary['total_feedback']}")
        print(f"Average score: {summary['avg_score']:.2f}/5")

        print("\nScore distribution:")
        for score, count in summary["score_distribution"].items():
            bar = "█" * count
            print(f"  {score} stars: {bar} ({count})")

        print("\nInsights:")
        for insight in self.get_insights():
            print(f"  • {insight}")
