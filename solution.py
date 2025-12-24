import os
import json
from collections import deque, defaultdict

def solve():
    # Load Data
    with open("metadata.json", "r") as f:
        metadata = json.load(f)
    with open("node_configs.json", "r") as f:
        node_configs = json.load(f)
        
    adj = defaultdict(list)
    in_degree = defaultdict(int)
    nodes = list(metadata.keys())
    
    # Load Explicit Dependencies
    for node in nodes:
        path = f"network_map/{node}.txt"
        if os.path.exists(path):
            with open(path, "r") as f:
                deps = [line.strip() for line in f if line.strip()]
                for dep in deps:
                    adj[dep].append(node)
                    in_degree[node] += 1

    # Add Implicit Dependencies (DB before Frontend in same region)
    region_nodes = defaultdict(# List of (type, name)
        lambda: {"Database": [], "Frontend": []}
    )
    for node, meta in metadata.items():
        region_nodes[meta["Region"]][meta["Type"]].append(node)
        
    for region, types in region_nodes.items():
        dbs = types["Database"]
        fes = types["Frontend"]
        for db in dbs:
            for fe in fes:
                # To avoid redundant deps, only if not already path
                # But for simplicity in solver, we just add it
                adj[db].append(fe)
                in_degree[fe] += 1

    # Weighted Critical Path (No resource caps)
    memo = {}
    def get_weighted_path(u):
        if u in memo: return memo[u]
        max_dist = 0
        for v in adj[u]:
            max_dist = max(max_dist, get_weighted_path(v))
        memo[u] = node_configs[u]["duration"] + max_dist
        return memo[u]

    weighted_cp_sum = 0
    if nodes:
        weighted_cp_sum = max(get_weighted_path(n) for n in nodes)

    # Simulation for Total Days (Respecting caps)
    day = 0
    completed = set()
    active = [] # List of (node, remaining_days)
    
    current_in_degree = in_degree.copy()
    
    while len(completed) < len(nodes):
        day += 1
        
        # 1. Update active migrations
        still_active = []
        for node, rem in active:
            if rem > 1:
                still_active.append((node, rem - 1))
            else:
                # Finished today
                completed.add(node)
                for neighbor in adj[node]:
                    current_in_degree[neighbor] -= 1
        active = still_active
        
        # 2. Start new migrations
        # Find candidates (ready to start)
        ready = [n for n in nodes if current_in_degree[n] == 0 and n not in completed and n not in [a[0] for a in active]]
        ready.sort() # Determinism
        
        for node in ready:
            # Check Global RU Cap (15)
            current_ru = sum(node_configs[a[0]]["ru_cost"] for a in active)
            if current_ru + node_configs[node]["ru_cost"] > 15:
                continue
            
            # Check Regional Concurrency (2)
            region = metadata[node]["Region"]
            reg_count = sum(1 for a in active if metadata[a[0]]["Region"] == region)
            if reg_count >= 2:
                continue
            
            # Start it
            active.append((node, node_configs[node]["duration"]))

    result = {
        "total_migration_days": day,
        "weighted_critical_path_sum": weighted_cp_sum,
        "total_nodes": len(nodes)
    }
    
    with open("result.json", "w") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    solve()
