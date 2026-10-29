"""
Unified Evaluation Runner: Adaptive Dengue Surveillance & Intervention Coordinator
Group 9 AI Course Project - Mid-Evaluation Demonstrator

Executes all five core AI course modules in sequence:
  1. Search & Constraint Satisfaction Problem (CSP)
  2. Classical Planning (STRIPS / PDDL)
  3. Reasoning Under Uncertainty (Bayesian Networks)
  4. Reinforcement Learning (Q-Learning)
  5. Generative AI Multi-Agent Coordinator
"""

import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.synthetic_generator import generate_mock_datasets
from modules.m1_search_csp import run_module_1
from modules.m2_planning import run_module_2
from modules.m3_bayes_net import run_module_3
from modules.m4_reinforcement import run_module_4
from modules.m5_genai_agents import run_module_5


def main():
    print("#" * 78)
    print("#  AI COURSE PROJECT: ADAPTIVE DENGUE SURVEILLANCE & INTERVENTION COORDINATOR")
    print("#  Group 9 - Mid-Evaluation Master Execution Suite")
    print("#" * 78)

    print("\n>>> STEP 0: Generating / Verifying Synthetic Data (OpenDengue Compatible)...")
    generate_mock_datasets()

    print("\n>>> STEP 1: Executing Module 1 (Search & CSP)...")
    run_module_1()

    print("\n>>> STEP 2: Executing Module 2 (Classical Planning)...")
    run_module_2()

    print("\n>>> STEP 3: Executing Module 3 (Reasoning Under Uncertainty / Bayes Net)...")
    run_module_3()

    print("\n>>> STEP 4: Executing Module 4 (Reinforcement Learning / Q-Learning)...")
    run_module_4()

    print("\n>>> STEP 5: Executing Module 5 (GenAI Multi-Agent Coordinator)...")
    run_module_5()

    print("\n" + "#" * 78)
    print("# [ALL 5 AI COURSE MODULES SUCCESSFULLY DEMONSTRATED FOR MID-EVALUATION]")
    print("#" * 78)


if __name__ == "__main__":
    main()

