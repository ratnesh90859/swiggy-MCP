# Swiggy Multi-Agent Test Suite

This folder contains a production-grade automated testing framework for the Swiggy Multi-Agent system.

## Structure
- `test_cases.py`: Define your multi-turn scenarios here in JSON format.
- `result_manager.py`: Logic for saving results to CSV.
- `test_runner.py`: The main script to execute tests.
- `test_results.csv`: Generated report of the latest test run.

## How to Run
Ensure your mock servers are running, then execute:

```bash
uv run python tests/test_runner.py
```

## Turn Validation
The runner checks for `PASS` (all expected tools called), `PARTIAL` (at least one tool called/agent reached), or `FAIL` (no tools called). Results include the full list of `tools_called` for audit.
