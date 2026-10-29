# Adaptive Dengue Surveillance and Intervention Coordinator (Group 9)

**AI Course Project — Mid-Evaluation Implementation Suite**

---

## 1. Executive Summary

This repository implements the **Adaptive Dengue Surveillance and Intervention Coordinator** designed for urban public health resource allocation. The system coordinates mosquito vector-control, rapid testing, and hospital bed buffers across urban districts by synthesizing surveillance data, mobility networks, and environmental factors.

For the **Mid-Evaluation**, this repository delivers working, standalone implementations of all **five core AI course modules**, backed by synthetic OpenDengue-compatible data schemas and automated test suites:

1. **Search & CSP (Module 1)**: Spatial contagion cluster identification (BFS/Dijkstra) and resource allocation under hard budget/team constraints (`python-constraint`).
2. **Classical Planning (Module 2)**: STRIPS / PDDL progression state-space planner enforcing preconditions (`Inspect -> Confirm -> Spray -> Treat -> Certify`).
3. **Reasoning Under Uncertainty (Module 3)**: Bayesian Network with DAG topology and CPTs modeling `Rainfall -> Mosquito_Density -> Dengue_Risk` (`pgmpy` Variable Elimination).
4. **Reinforcement Learning (Module 4)**: Tabular Q-learning agent with an empirical upward reward learning curve (+240+ reward improvement).
5. **Generative AI Multi-Agent Coordinator (Module 5)**: Role-specialized multi-agent system coordinating Central Emergency Response, Tactical Field Operations, and Public Health Advisories.

---

## 2. Repository Structure

```
Dengue-Intervention/
├── .venv/                      # Python 3.11 virtual environment
├── requirements.txt           # Python package dependencies
├── run_all_modules.py         # Unified master demonstrator running all 5 modules
├── README.md                  # Comprehensive setup, run, and evaluation documentation
├── data/
│   ├── synthetic_generator.py # Generates OpenDengue-compatible mock CSVs
│   ├── districts_mock.csv     # 10 urban districts with cases, beds, rainfall, costs
│   └── weather_timeseries.csv # 14-day rainfall, temperature, and ovitrap counts
├── modules/
│   ├── m1_search_csp.py       # Module 1: Graph Search & CSP Resource Allocation
│   ├── m2_planning.py         # Module 2: Classical STRIPS/PDDL Progression Planner
│   ├── m3_bayes_net.py        # Module 3: Bayesian Network & Variable Elimination
│   ├── m4_reinforcement.py    # Module 4: Adaptive Q-Learning MDP Agent
│   └── m5_genai_agents.py     # Module 5: Multi-Agent Prompt Orchestration
├── pddl/
│   ├── domain.pddl            # Formal PDDL Domain definition
│   └── problem.pddl           # Formal PDDL Problem definition
└── tests/
    └── test_modules.py        # Pytest sanity test suite covering all modules
```

---

## 3. Environment Setup & Installation

### Step 1: Activate the Virtual Environment (`.venv`)

A dedicated Python 3.11 virtual environment (`.venv`) is configured.

**Windows PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

### Step 2: Install Dependencies (Already Pre-installed)

If installing in a fresh environment:
```bash
pip install -r requirements.txt
```

---

## 4. Execution Guide & Demonstration Commands

### Option A: Run All 5 Modules Simultaneously (Recommended for Mid-Eval Demo)
```bash
python run_all_modules.py
```

### Option B: Run Individual AI Modules

#### Module 1: Graph Search & CSP Resource Allocation
```bash
python modules/m1_search_csp.py
```
* **Concepts Demonstrated:**
  * Spatial network graph traversal using BFS for outbreak cluster identification.
  * Dijkstra shortest route calculation from depot to target outbreak zones.
  * Constraint Satisfaction Problem (CSP) with variable domain `{0, 1, 2}` teams per district.
  * Hard budget constraints ($\le \$10,000$) and high-risk team guarantees.
  * **Failure Demonstration:** Proves problem is **UNSATISFIABLE** when budget is constrained below required risk mitigation thresholds ($\$1,000$).

#### Module 2: Classical Planning (STRIPS / PDDL Engine)
```bash
python modules/m2_planning.py
```
* **Concepts Demonstrated:**
  * Forward State-Space Search (Progression Planning).
  * Strict action preconditions and effects: `At(Team, Loc)`, `InspectBreedingSites(Loc)`, `SprayLarvicide(Loc)`, `DeployMedicalTreatment(Loc)`, `CertifyZoneSafe(Loc)`.
  * **Precondition Violation Test:** Proves plan is impossible/unreachable when road connectivity is severed or inspection has not occurred.

#### Module 3: Reasoning Under Uncertainty (Bayesian Network)
```bash
python modules/m3_bayes_net.py
```
* **Concepts Demonstrated:**
  * Directed Acyclic Graph (DAG): `Rainfall -> Mosquito_Density`, `Mosquito_Density + Mobility -> Dengue_Risk`.
  * Full Conditional Probability Tables (CPTs) printed and inspected.
  * Exact Inference using **Variable Elimination**:
    * Unconditional Prior: $P(\text{Risk}=\text{High}) = 0.4125$
    * Forward Causal Query: $P(\text{Risk}=\text{High} \mid \text{Rainfall}=\text{High}) = 0.6562$
    * Compounding Risk: $P(\text{Risk}=\text{High} \mid \text{Rain}=\text{High}, \text{Mobility}=\text{High}) = 0.7950$
    * Diagnostic (Inverse) Query: $P(\text{Rainfall}=\text{High} \mid \text{Risk}=\text{High}) = 0.6364$

#### Module 4: Reinforcement Learning (Adaptive Q-Learning)
```bash
python modules/m4_reinforcement.py
```
* **Concepts Demonstrated:**
  * Markov Decision Process (MDP) with 4 actions: Move, Intensive Spray, Fog Containment, Passive Hold.
  * Temporal Difference (TD) Q-learning update with $\epsilon$-greedy exploration decay.
  * **Empirical Convergence:** Shows mean rewards climbing from $-1.70$ (episodes 1–100) to $+238.95$ (episodes 701–800) for a net performance gain of $+240+$ units.
  * Displays learned Q-values and optimal policies for critical states.

#### Module 5: Generative AI Multi-Agent Coordinator
```bash
python modules/m5_genai_agents.py
```
* **Concepts Demonstrated:**
  * Role-specialized multi-agent system:
    1. *Central Emergency Response Coordinator*: Synthesizes risk scores and resource quotas into strategic code-red directives.
    2. *Tactical Field Operations Commander*: Converts directives into tactical checklists (PPE gear, BTI dosage, equipment).
    3. *Public Health Communications Officer*: Generates localized community health advisories and symptom checklists for citizens.
  * Resilient offline generator ensuring zero reliance on paid API tokens during grading.

---

## 5. Automated Sanity Test Suite

Run unit and integration tests across all modules using `pytest`:
```bash
pytest tests/
```
Output:
```
tests/test_modules.py ...... [100%]
6 passed in ~3s
```

---

## 6. Faculty Q&A Preparation

* **Q1: Why are the modules standalone rather than fully integrated for the mid-evaluation?**
  * *A: As stated in the mid-evaluation guidelines, the primary objective is to assess progress and conceptual rigor across each of the five mandatory AI paradigms independently before coupling them into an end-to-end pipeline in Milestone 2.*
* **Q2: How does the Bayesian Network relate to course concepts?**
  * *A: It represents a noisy causal model using a Directed Acyclic Graph (DAG) and Tabular CPTs. We utilize Variable Elimination for exact probabilistic inference, demonstrating how evidence updates prior beliefs via Bayes' Rule.*
* **Q3: Why formulate resource allocation as a CSP rather than simple sorting?**
  * *A: CSP allows hard constraint enforcement (maximum personnel, total budget, hospital bed buffers, and mandatory coverage for high-risk zones) that can formally detect when constraints are unsatisfiable and require budget reallocation.*
* **Q4: Why use Reinforcement Learning instead of static heuristic rules?**
  * *A: Vector control is a sequential decision process where actions taken today alter future state distributions (e.g. chemical depletion vs epidemic escalation). Tabular Q-learning learns the discounted future return, optimizing multi-step interventions.*

---

## 7. Team Responsibility Matrix (Group 9)

| Member | Module / Role | Exact Deliverable | Demo Responsibility |
|---|---|---|---|
| **M1** | Project Lead / Architect | Repo setup, `.venv`, `requirements.txt`, `run_all_modules.py` | Architecture overview, data flow |
| **M2** | Search / CSP Lead | `modules/m1_search_csp.py` (CSP Formulation) | Demonstrating CSP feasible allocations |
| **M3** | Search / CSP Support | `modules/m1_search_csp.py` (Graph Search & BFS) | Explaining constraint failure ($1,000 budget) |
| **M4** | Planning Lead | `modules/m2_planning.py`, `pddl/domain.pddl` | Demonstrating 5-step progression plan |
| **M5** | Planning Support | `pddl/problem.pddl`, precondition test cases | Explaining severed path / unmet preconditions |
| **M6** | Uncertainty Lead | `modules/m3_bayes_net.py` (DAG & CPTs) | Demonstrating Variable Elimination queries |
| **M7** | Uncertainty Support | `modules/m3_bayes_net.py` (Diagnostic inference) | Explaining Bayes Rule probability shifts |
| **M8** | RL Lead | `modules/m4_reinforcement.py` (MDP & Q-Learning) | Showing reward convergence (+240 gain) |
| **M9** | GenAI Lead | `modules/m5_genai_agents.py` (Multi-Agent System) | Demonstrating 3-agent coordinated advisory |
| **M10** | QA & Evaluation Lead | `tests/test_modules.py`, presentation slides | Running pytest and presenting next steps |
