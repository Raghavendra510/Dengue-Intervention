"""
Module 3: Reasoning Under Uncertainty (Bayesian Networks)
Course Concepts:
  - Directed Acyclic Graphs (DAGs) representing causal dependencies.
  - Conditional Probability Tables (CPTs).
  - Exact probabilistic inference using Variable Elimination.
  - Diagnostic vs Causal Reasoning.
"""

import sys
import warnings
warnings.filterwarnings('ignore')
try:
    from pgmpy.models import DiscreteBayesianNetwork as BayesianNetwork
except ImportError:
    from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination


def build_dengue_bayesian_network():
    """
    Constructs the causal Bayesian Network:
       Rainfall --------> Mosquito_Density
                               |
                               v
      Human_Mobility ----> Dengue_Risk
    """
    model = BayesianNetwork([
        ('Rainfall', 'Mosquito_Density'),
        ('Mosquito_Density', 'Dengue_Risk'),
        ('Human_Mobility', 'Dengue_Risk')
    ])

    # 1. P(Rainfall): Prior probability of rainfall level
    # States: [0: 'Low', 1: 'High']
    cpd_rainfall = TabularCPD(
        variable='Rainfall',
        variable_card=2,
        values=[[0.60], [0.40]],
        state_names={'Rainfall': ['Low', 'High']}
    )

    # 2. P(Human_Mobility): Prior probability of inter-district commuting
    # States: [0: 'Low', 1: 'High']
    cpd_mobility = TabularCPD(
        variable='Human_Mobility',
        variable_card=2,
        values=[[0.50], [0.50]],
        state_names={'Human_Mobility': ['Low', 'High']}
    )

    # 3. P(Mosquito_Density | Rainfall)
    # Heavy rainfall creates stagnant pools, multiplying mosquito larvae
    cpd_mosquito = TabularCPD(
        variable='Mosquito_Density',
        variable_card=2,
        values=[
            [0.80, 0.15],  # Low mosquito: Rain=Low (80%), Rain=High (15%)
            [0.20, 0.85]   # High mosquito: Rain=Low (20%), Rain=High (85%)
        ],
        evidence=['Rainfall'],
        evidence_card=[2],
        state_names={
            'Mosquito_Density': ['Low', 'High'],
            'Rainfall': ['Low', 'High']
        }
    )

    # 4. P(Dengue_Risk | Mosquito_Density, Human_Mobility)
    # Both vectors and host mobility amplify transmission risk
    cpd_risk = TabularCPD(
        variable='Dengue_Risk',
        variable_card=2,
        values=[
            # [Mosq=Low/Mob=Low, Mosq=Low/Mob=High, Mosq=High/Mob=Low, Mosq=High/Mob=High]
            [0.95, 0.80, 0.40, 0.10],  # Risk = Low
            [0.05, 0.20, 0.60, 0.90]   # Risk = High
        ],
        evidence=['Mosquito_Density', 'Human_Mobility'],
        evidence_card=[2, 2],
        state_names={
            'Dengue_Risk': ['Low', 'High'],
            'Mosquito_Density': ['Low', 'High'],
            'Human_Mobility': ['Low', 'High']
        }
    )

    model.add_cpds(cpd_rainfall, cpd_mobility, cpd_mosquito, cpd_risk)
    assert model.check_model(), "Bayesian Network topology or CPT probabilities are inconsistent!"
    return model


def infer_outbreak_risk(model, evidence=None):
    """Performs exact inference using Variable Elimination."""
    infer = VariableElimination(model)
    query_result = infer.query(variables=['Dengue_Risk'], evidence=evidence if evidence else {})
    return query_result


def run_module_3():
    print("=" * 70)
    print("MODULE 3: REASONING UNDER UNCERTAINTY (BAYESIAN NETWORKS)")
    print("=" * 70)

    model = build_dengue_bayesian_network()

    print("\n[BAYESIAN NETWORK TOPOLOGY]")
    print(f"Nodes: {model.nodes()}")
    print(f"Edges (Causal dependencies): {model.edges()}")

    print("\n[CONDITIONAL PROBABILITY TABLES (CPTs)]")
    for cpd in model.get_cpds():
        print(f"\n--- CPD: P({cpd.variable} | {', '.join(cpd.variables[1:]) or 'None'}) ---")
        print(cpd)

    infer = VariableElimination(model)

    print("\n[EXACT INFERENCE EXPERIMENTS (Variable Elimination)]")

    # Experiment 1: Prior (Baseline without evidence)
    q1 = infer.query(variables=['Dengue_Risk'])
    p_risk_high_baseline = q1.values[1]
    print(f"1. Prior Unconditional Risk: P(Dengue_Risk=High) = {p_risk_high_baseline:.4f}")

    # Experiment 2: Evidence of Heavy Rainfall
    q2 = infer.query(variables=['Dengue_Risk'], evidence={'Rainfall': 'High'})
    p_risk_high_rain = q2.values[1]
    print(f"2. Causal Forward Query   : P(Dengue_Risk=High | Rainfall=High) = {p_risk_high_rain:.4f}")

    # Experiment 3: Compounding Evidence (Heavy Rainfall + High Mobility)
    q3 = infer.query(variables=['Dengue_Risk'], evidence={'Rainfall': 'High', 'Human_Mobility': 'High'})
    p_risk_high_compound = q3.values[1]
    print(f"3. Extreme Threat Query   : P(Dengue_Risk=High | Rain=High, Mobility=High) = {p_risk_high_compound:.4f}")

    # Experiment 4: Diagnostic / Explaining-Away Query (Inverse Reasoning)
    q4 = infer.query(variables=['Rainfall'], evidence={'Dengue_Risk': 'High'})
    p_rain_given_risk = q4.values[1]
    print(f"4. Diagnostic Query       : P(Rainfall=High | Dengue_Risk=High) = {p_rain_given_risk:.4f}")

    print("\n[VALIDATION OF BAYES RULE CONVERGENCE]")
    assert p_risk_high_compound > p_risk_high_rain > p_risk_high_baseline
    print(" [OK] PASS: Posterior probabilities mathematically update monotonically under compounding risk.")
    print("=" * 70)


if __name__ == "__main__":
    run_module_3()
