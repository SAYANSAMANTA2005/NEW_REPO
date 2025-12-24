import os
import json
import pytest

def test_result_exists():
    assert os.path.exists("result.json"), "result.json was not created"

def test_result_format():
    with open("result.json", "r") as f:
        data = json.load(f)
    
    assert "total_migration_days" in data
    assert "weighted_critical_path_sum" in data
    assert "total_nodes" in data
    assert data["total_nodes"] == 40

def test_correctness():
    with open("result.json", "r") as f:
        data = json.load(f)
    
    # Values for random.seed(42) and the hard solver logic
    assert data["total_migration_days"] == 56
    assert data["weighted_critical_path_sum"] == 51
