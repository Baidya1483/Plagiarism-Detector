# 📈 Intelligent Route Planner Using Graph Algorithms

A high-performance, professional-grade logistics system engineering tool built with Python to model complex urban road infrastructures as **Weighted Directed Graphs**, compute spatial alternative routes using **Multi-Criteria Optimization**, and manage dynamic grid constraints at runtime. This project serves as a comprehensive portfolio piece demonstrating advanced graph theory, spatial searching, and clean backend engine microservice boundaries.

---

## 🚀 Overview

[cite_start]The **Intelligent Route Planner** addresses the scaling and multi-constraint calculation challenges faced by modern ride-hailing networks, supply chain platforms, and map applications[cite: 564, 776]. Traditional shortest-path tools focus strictly on static distance weights, causing them to break down when handling real-world factors like peak hour traffic surges, active toll pricing boundaries, turn rules, or sudden road closures.

[cite_start]This project provides a robust, extensible route-planning engine by modeling cities using spatial adjacency lists[cite: 545, 619]. [cite_start]By structuring edge weights around pluggable metric functions (travel duration, distance, road classification metrics, and tolls), the routing system exposes pluggable single and composite travel configurations effortlessly[cite: 545, 836].


### ✨ Key Features
* [cite_start]**Adjacency-List Directed Graph Core**: Modeled using a lean, directional spatial memory outline optimized for space-efficient sparse road network representations[cite: 1146].
* [cite_start]**A* Heuristic Spatial Search Speed-ups**: Combines a vectorized Haversine straight-line duration estimator with standard Dijkstra implementations to minimize node traversal space and speed up queries[cite: 870, 887].
* **Pluggable Optimization Objectives**: Automatically computes optimized routes optimized for Fastest time, Shortest distance, Lowest Toll costs, and Eco-friendly emissions[cite: 545].
* [cite_start]**Multi-Criteria Pareto Frontiers**: Tracks alternative, non-dominated path combinations to let drivers weigh travel speed against total toll expenditure constraints[cite: 908, 919].
* [cite_start]**State-Space Turn Penalties**: Implements a modified node-orientation queue wrapper to factor in turn-delay penalties at intersections, mimicking commercial GPS architectures[cite: 935, 948].
* **Dynamic Grid Mutation Safety**: Runs real-time incident injections (such as temporary bottleneck congestion updates or complete structural edge closures) on isolated graph memory copies, avoiding core topology corruption errors[cite: 935, 1008].

---

## 🛠️ Tech Stack
* [cite_start]**Language**: Python 3.11+ [cite: 579]
* [cite_start]**Graph Topology Modeling Suite**: NetworkX [cite: 586, 841]
* **Data Processing Framework**: Pandas, NumPy Matrix Allocators
* [cite_start]**Microservice API Layer**: FastAPI, Pydantic Data Contract Systems, Uvicorn Engines [cite: 785]
* [cite_start]**Validation Subsystems**: Pytest Test Coverage Frameworks [cite: 1078]

---

## 🏗️ Project Structure
```text
Intelligent-Route-Planner-Graph-Algorithms/
[cite_start]├── data/                      # Persistent data lakes for topology map CSV sheets [cite: 638]
[cite_start]├── outputs/                   # Performance diagnostic logs and data manifests [cite: 640]
[cite_start]├── src/                       # Modular Python system logic modules [cite: 639]
[cite_start]│   ├── data_builder.py        # Spatial city matrix synthesis drivers [cite: 796]
[cite_start]│   ├── graph_loader.py        # Adjacency-list directed graph loader components [cite: 839]
[cite_start]│   ├── router.py              # Single-objective A* and Dijkstra calculation cores [cite: 869]
│   ├── multicriteria.py       # Pareto front and composite sum model definitions [cite: 903]
│   ├── dynamics.py            # Turn penalties and dynamic traffic incident handlers [cite: 935]
│   └── test_routing.py        # Automated validation test cases tracking paths [cite: 1078]
├── main.py                    # Real-time FastAPI backend endpoint routes [cite: 646, 785]
├── requirements.txt           # Unified dependency version blueprints [cite: 644]
└── README.md                  # Detailed project presentation dashboard [cite: 643]