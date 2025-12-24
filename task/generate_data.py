import os
import json
import random

def generate_hard_data():
    random.seed(42) # Deterministic
    os.makedirs("network_map", exist_ok=True)
    
    regions = ["US-East", "EU-West", "Asia-South", "Global-Core"]
    node_types = ["Database", "Frontend"]
    
    nodes = [f"node_{i:02d}" for i in range(40)]
    metadata = {}
    node_configs = {}
    
    # Assign metadata
    for i, node in enumerate(nodes):
        region = regions[i // 10]
        ntype = "Database" if (i % 10) < 4 else "Frontend" # 4 DBs, 6 FEs per region
        metadata[node] = {"Region": region, "Type": ntype}
        
        node_configs[node] = {
            "duration": random.randint(1, 4),
            "ru_cost": random.randint(2, 5)
        }

    # Create DAG Dependencies (Explicit)
    # Ensure it's a valid DAG by only depending on previous indices
    dependencies = {node: [] for node in nodes}
    for i in range(1, 40):
        if i % 5 == 0: continue # Break some chains
        num_deps = random.randint(1, 2)
        # Prefer dependencies within the same region or on the Global-Core (0-9)
        possible = list(range(max(0, i-5), i))
        if not possible: continue
        dep_indices = random.sample(possible, min(len(possible), num_deps))
        dependencies[nodes[i]] = [nodes[idx] for idx in dep_indices]

    # Write files
    for node, deps in dependencies.items():
        with open(f"network_map/{node}.txt", "w") as f:
            f.write("\n".join(deps))
            
    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
        
    with open("node_configs.json", "w") as f:
        json.dump(node_configs, f, indent=2)

if __name__ == "__main__":
    generate_hard_data()
