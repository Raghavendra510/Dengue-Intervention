"""
Module 1: Spatial Graph Search & Constraint Satisfaction Problem (CSP)
Course Concepts:
  - Graph Search (BFS / Dijkstra / A*): Identifies outbreak transmission clusters
    and finds shortest path between mobile response depots and target zones.
  - Constraint Satisfaction Problem (CSP): Allocates vector-control and medical
    resources subject to hard budget, personnel, and priority constraints using python-constraint.
"""

import os
import sys
import pandas as pd
import networkx as nx
from collections import deque
from constraint import Problem, ExactSumConstraint, MaxSumConstraint

def load_data(filepath=None):
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), "..", "data", "districts_mock.csv")
    if not os.path.exists(filepath):
        from data.synthetic_generator import generate_mock_datasets
        generate_mock_datasets()
    return pd.read_csv(filepath)

# ---------------------------------------------------------
# Part A: Spatial Graph Search (BFS & Cluster Identification)
# ---------------------------------------------------------

def build_spatial_graph(df):
    """Constructs NetworkX graph of district connectivity."""
    G = nx.Graph()
    for _, row in df.iterrows():
        d_id = row["District_ID"]
        G.add_node(d_id, 
                   name=row["District_Name"],
                   cases=row["Reported_Cases"],
                   risk=row["Baseline_Risk"],
                   beds=row["Hospital_Beds"])
        neighbors = [n.strip() for n in str(row["Neighbors"]).split(",") if n.strip()]
        for n in neighbors:
            G.add_edge(d_id, n, weight=1.0)
    return G

def find_outbreak_cluster(G, start_district, risk_threshold="High"):
    """
    Breadth-First Search (BFS) to identify connected active contagion clusters.
    Traverses neighboring districts that also exhibit high risk.
    """
    visited = set([start_district])
    queue = deque([start_district])
    cluster = []

    while queue:
        curr = queue.popleft()
        cluster.append(curr)
        for neighbor in G.neighbors(curr):
            if neighbor not in visited:
                visited.add(neighbor)
                # Expand cluster if neighbor is high risk or has significant cases
                if G.nodes[neighbor].get("risk") == risk_threshold:
                    queue.append(neighbor)
    return cluster

def shortest_intervention_route(G, depot_district, target_district):
    """
    Dijkstra / Uniform Cost Search to find the fastest dispatch path
    from the regional HQ / depot to a quarantined or critical district.
    """
    try:
        path = nx.shortest_path(G, source=depot_district, target=target_district, weight="weight")
        return path
    except nx.NetworkXNoPath:
        return None

# ---------------------------------------------------------
# Part B: Constraint Satisfaction Problem (CSP) Formulation
# ---------------------------------------------------------

def solve_resource_csp(df, max_total_teams=8, total_budget=10000, force_insufficient=False):
    """
    Formulates resource allocation as a CSP:
      - Variables: District IDs (e.g., D01..D10)
      - Domain: {0, 1, 2} teams deployable to each district
      - Constraints:
          1. Total teams <= max_total_teams
          2. Sum(teams * Spraying_Cost) <= total_budget
          3. High risk districts MUST have >= 1 team
          4. Severe outbreaks (cases > 100) MUST have 2 teams
    """
    problem = Problem()
    variables = df["District_ID"].tolist()
    cost_map = dict(zip(df["District_ID"], df["Spraying_Cost"]))
    risk_map = dict(zip(df["District_ID"], df["Baseline_Risk"]))
    cases_map = dict(zip(df["District_ID"], df["Reported_Cases"]))

    # Domain: Number of intervention teams
    team_domain = [0, 1, 2]
    for var in variables:
        problem.addVariable(var, team_domain)

    # 1. Total Teams Constraint: sum(teams) <= max_total_teams
    def total_teams_constraint(*teams):
        return sum(teams) <= max_total_teams

    problem.addConstraint(total_teams_constraint, variables)

    # 2. Total Budget Constraint: sum(teams[i] * cost[i]) <= total_budget
    if force_insufficient:
        # Demonstrate unsatisfiable constraint
        effective_budget = 1000
    else:
        effective_budget = total_budget

    def budget_constraint(*teams):
        total_expenditure = sum(t * cost_map[v] for t, v in zip(teams, variables))
        return total_expenditure <= effective_budget

    problem.addConstraint(budget_constraint, variables)

    # 3. High Risk Priority: High-risk districts must receive at least 1 team
    for var in variables:
        if risk_map[var] == "High":
            def min_team_req(t):
                return t >= 1
            problem.addConstraint(min_team_req, [var])

    # 4. Critical Case Count Constraint: If cases > 100, require 2 teams if budget permits
    if not force_insufficient:
        for var in variables:
            if cases_map[var] > 100:
                def critical_team_req(t):
                    return t == 2
                problem.addConstraint(critical_team_req, [var])

    solutions = problem.getSolutions()
    return solutions, effective_budget

# ---------------------------------------------------------
# Demonstration Runner
# ---------------------------------------------------------

def run_module_1():
    print("=" * 70)
    print("MODULE 1: GRAPH SEARCH & CONSTRAINT SATISFACTION PROBLEM (CSP)")
    print("=" * 70)

    df = load_data()
    G = build_spatial_graph(df)

    print("\n[PART 1: GRAPH SEARCH & CONTAGION CLUSTERING]")
    print(f"Total Districts (Nodes): {G.number_of_nodes()}, Spatial Adjacencies (Edges): {G.number_of_edges()}")

    start_node = "D02"
    cluster = find_outbreak_cluster(G, start_node, risk_threshold="High")
    print(f" -> BFS Outbreak Cluster from {start_node} ({G.nodes[start_node]['name']}): {cluster}")

    depot = "D01"
    target = "D10"
    route = shortest_intervention_route(G, depot, target)
    print(f" -> Shortest Intervention Route (Dijkstra) from Depot {depot} to Target {target}: {' -> '.join(route)}")

    print("\n[PART 2: CSP RESOURCE ALLOCATION SOLVER]")
    print("Test Scenario A: Feasible Budget ($10,000, Max Teams = 8)")
    solutions, budget = solve_resource_csp(df, max_total_teams=8, total_budget=10000, force_insufficient=False)
    print(f" -> Total Feasible Solutions Found: {len(solutions)}")
    if solutions:
        best_sol = solutions[0]
        cost_map = dict(zip(df["District_ID"], df["Spraying_Cost"]))
        total_cost = sum(best_sol[d] * cost_map[d] for d in best_sol)
        total_teams = sum(best_sol.values())
        print(f" -> Sample Feasible Allocation (Teams: {total_teams}/8, Budget Used: ${total_cost}/${budget}):")
        for d in sorted(best_sol.keys()):
            cases = df.loc[df['District_ID'] == d, 'Reported_Cases'].values[0]
            risk = df.loc[df['District_ID'] == d, 'Baseline_Risk'].values[0]
            print(f"    - District {d} ({risk} Risk, {cases:3d} cases): {best_sol[d]} teams assigned")

    print("\nTest Scenario B: Constraint Failure Demonstration (Unsatisfiable Budget $1,000)")
    insufficient_sols, bad_budget = solve_resource_csp(df, max_total_teams=8, total_budget=1000, force_insufficient=True)
    print(f" -> Solutions Found with Budget ${bad_budget}: {len(insufficient_sols)}")
    if len(insufficient_sols) == 0:
        print(" [OK] PASS: CSP correctly proved UNSATISFIABLE when resources violate minimum risk mandates.")

    print("=" * 70)

if __name__ == "__main__":
    run_module_1()
