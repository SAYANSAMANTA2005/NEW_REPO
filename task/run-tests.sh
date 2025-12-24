#!/bin/bash
# run-tests.sh
# Run the solution and then the tests

echo "Starting task execution..."
bash solution.sh

echo "Running validation tests..."
pytest tests/test_output.py
