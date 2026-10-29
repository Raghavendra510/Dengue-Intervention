"""
Sanity and Verification Tests for Dengue Surveillance & Intervention Coordinator
Executes unit and integration tests across all five mandatory AI course modules.
"""

import os
import sys
import pytest

# Ensure modules package is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.synthetic_generator import generate_mock_datasets
from modules.m1_search_csp import load_data, build_spatial_graph, find_outbreak_cluster, solve_resource_csp
from modules.m2_planning import setup_dengue_planning_domain
from modules.m3_bayes_net import build_dengue_bayesian_network
from modules.m4_reinforcement import DengueInterventionEnv, QLearningAgent
from modules.m5_genai_agents import DengueMultiAgentSystem


def test_synthetic_data_generation():
    dist_csv, weather_csv = generate_mock_datasets()
    assert os.path.exists(dist_csv), "districts_mock.csv was not created!"
    assert os.path.exists(weather_csv), "weather_timeseries.csv was not created!"


def test_m1_search_csp():
    df = load_data()
    G = build_spatial_graph(df)
    assert G.number_of_nodes() == 10
    assert G.number_of_edges() > 0

    cluster = find_outbreak_cluster(G, "D02", risk_threshold="High")
    assert "D02" in cluster

    # Feasible CSP test
    sols, _ = solve_resource_csp(df, max_total_teams=8, total_budget=10000, force_insufficient=False)
    assert len(sols) > 0, "CSP solver should find feasible allocations under $10,000 budget."

    # Infeasible CSP test
    bad_sols, _ = solve_resource_csp(df, max_total_teams=8, total_budget=1000, force_insufficient=True)
    assert len(bad_sols) == 0, "CSP solver must report 0 solutions under insufficient $1,000 budget."


def test_m2_planning():
    districts = ["D01", "D02"]
    adjacencies = [("D01", "D02"), ("D02", "D01")]
    teams = ["Team_Alpha"]
    planner = setup_dengue_planning_domain(districts, adjacencies, teams)

    init_state = {
        "At(Team_Alpha, D01)",
        "Adjacent(D01, D02)",
        "Adjacent(D02, D01)",
        "Uninspected(D02)"
    }
    goal_state = {"Safe(D02)"}

    plan = planner.plan(init_state, goal_state)
    assert plan is not None, "Classical planner failed to find valid intervention sequence!"
    assert len(plan) == 5, f"Expected 5-step plan, got {len(plan)}"

    # Test failure with missing preconditions (unreachable)
    severed_state = {"At(Team_Alpha, D01)", "Uninspected(D02)"} # Missing adjacency!
    failed_plan = planner.plan(severed_state, goal_state)
    assert failed_plan is None, "Planner should not find plan when movement precondition is unsatisfied."


def test_m3_bayes_net():
    from pgmpy.inference import VariableElimination
    model = build_dengue_bayesian_network()
    assert model.check_model()

    infer = VariableElimination(model)
    q_prior = infer.query(variables=['Dengue_Risk'])
    q_compound = infer.query(variables=['Dengue_Risk'], evidence={'Rainfall': 'High', 'Human_Mobility': 'High'})

    p_prior = q_prior.values[1]
    p_compound = q_compound.values[1]
    assert p_compound > p_prior, "High rain and mobility must elevate posterior risk above prior!"


def test_m4_reinforcement():
    env = DengueInterventionEnv()
    agent = QLearningAgent()
    state = env.reset()
    assert len(state) == 3

    action = agent.choose_action(state)
    next_state, reward, done = env.step(action)
    agent.update(state, action, reward, next_state, done)

    assert state in agent.q_table
    assert len(agent.q_table[state]) == 4


def test_m5_genai_coordination():
    mas = DengueMultiAgentSystem(use_api=False)
    directive = mas.coordinator_agent({"high_risk_zones": ["Riverside Slums (D02)"]})
    assert "CENTRAL COORDINATOR SITUATION DIRECTIVE" in directive

    field_order = mas.field_operations_agent(directive, "Riverside Slums (D02)")
    assert "FIELD OPERATIONS TACTICAL SQUAD" in field_order

    advisory = mas.public_health_advisor_agent("Riverside Slums", "HIGH")
    assert "COMMUNITY HEALTH ADVISORY" in advisory

