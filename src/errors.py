import time


class ErrorTracker:
    """Track and analyze errors in workflows"""

    ERROR_TYPES = {
        "timeout": ["timeout", "timed out", "deadline"],
        "rate_limit": ["rate limit", "too many requests", "throttle"],
        "token_limit": ["token limit", "context length", "max tokens"],
        "auth": ["authentication", "unauthorized", "credentials"],
        "network": ["connection", "network", "unreachable"],
        "parsing": ["parse", "json", "format", "invalid"]
    }

    SOLUTIONS = {
        "timeout": [
            "Increase timeout settings",
            "Use async processing",
            "Break into smaller requests"
        ],
        "rate_limit": [
            "Implement exponential backoff",
            "Add request throttling",
            "Upgrade API tier"
        ],
        "token_limit": [
            "Implement text chunking",
            "Shorten prompts",
            "Use summarization"
        ],
        "auth": [
            "Check API key validity",
            "Verify credentials",
            "Check permissions"
        ],
        "network": [
            "Check connectivity",
            "Implement retries",
            "Add timeout handling"
        ],
        "parsing": [
            "Add input validation",
            "Use structured outputs",
            "Improve format instructions"
        ],
        "unknown": [
            "Review error logs",
            "Add more specific error handling",
            "Contact support if persistent"
        ]
    }

    def __init__(self):
        self.errors = []
        self.error_counts = {}

    def classify_error(self, error_message: str) -> str:
        """Classify error type based on message"""
        error_lower = error_message.lower()

        for error_type, keywords in self.ERROR_TYPES.items():
            if any(keyword in error_lower for keyword in keywords):
                return error_type

        return "unknown"

    def log_error(self, error_message: str, context: dict = None):
        """Log an error with context"""
        error_type = self.classify_error(error_message)

        error_entry = {
            "timestamp": time.time(),
            "type": error_type,
            "message": error_message,
            "context": context or {}
        }

        self.errors.append(error_entry)
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1

        return error_entry

    def get_summary(self) -> dict:
        """Get error summary"""
        if not self.errors:
            return {"total_errors": 0}

        return {
            "total_errors": len(self.errors),
            "by_type": dict(self.error_counts),
            "most_common": (max(self.error_counts.items(),
                            key=lambda x: x[1]) if self.error_counts else None)
        }

    def get_solutions(self) -> dict:
        """Get solutions for logged error types"""
        relevant_solutions = {}
        for error_type in self.error_counts.keys():
            if error_type in self.SOLUTIONS:
                relevant_solutions[error_type] = self.SOLUTIONS[error_type]

        return relevant_solutions

    def print_report(self):
        """Print error report"""
        print("\n" + "=" * 50)
        print("🚨 ERROR REPORT")
        print("=" * 50)

        summary = self.get_summary()
        print(f"\nTotal errors: {summary['total_errors']}")

        if summary['total_errors'] == 0:
            print("✅ No errors logged")
            return

        print("\nErrors by type:")
        for error_type, count in summary.get('by_type', {}).items():
            pct = (count / summary['total_errors']) * 100
            print(f"  {error_type}: {count} ({pct:.1f}%)")

        print("\nSuggested solutions:")
        solutions = self.get_solutions()
        for error_type, fixes in solutions.items():
            print(f"\n  {error_type.upper()}:")
            for fix in fixes:
                print(f"    - {fix}")
