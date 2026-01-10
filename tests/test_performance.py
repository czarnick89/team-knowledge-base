from src.performance import PerformanceMonitor


def test_monitor_creation():
    """Test monitor initialization"""
    monitor = PerformanceMonitor()

    assert monitor.runs == []
    assert monitor.step_metrics == {}


def test_record_run():
    """Test recording a workflow run"""
    monitor = PerformanceMonitor()

    state = {
        "query": "test",
        "execution_time": 5.0,
        "step_count": 3,
        "token_estimate": 500,
        "cost_estimate": 0.001,
        "error": None,
        "trace_metadata": {"steps": []}
    }

    monitor.record_run(state)

    assert len(monitor.runs) == 1
    assert monitor.runs[0]["execution_time"] == 5.0


def test_get_summary_empty():
    """Test summary with no runs"""
    monitor = PerformanceMonitor()
    summary = monitor.get_summary()

    assert summary["total_runs"] == 0


def test_get_summary_with_runs():
    """Test summary with recorded runs"""
    monitor = PerformanceMonitor()

    for i in range(3):
        state = {
            "query": f"test {i}",
            "execution_time": 3.0,
            "step_count": 2,
            "token_estimate": 300,
            "cost_estimate": 0.0006,
            "error": None,
            "trace_metadata": {"steps": []}
        }
        monitor.record_run(state)

    summary = monitor.get_summary()

    assert summary["total_runs"] == 3
    assert summary["avg_execution_time"] == 3.0


def test_get_recommendations_slow_step():
    """Test recommendations for slow steps"""
    monitor = PerformanceMonitor()

    state = {
        "query": "test",
        "execution_time": 10.0,
        "step_count": 1,
        "token_estimate": 100,
        "cost_estimate": 0.0002,
        "error": None,
        "trace_metadata": {
            "steps": [{
                "step_name": "research",
                "duration": 10.0,
                "tokens": 100,
                "status": "success"
            }]
        }
    }
    monitor.record_run(state)

    recommendations = monitor.get_recommendations()

    assert len(recommendations) > 0
    assert any(r["issue"] == "High latency" for r in recommendations)
