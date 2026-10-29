# Group 9 Mid-Evaluation Execution & Outputs Report
**Project**: Adaptive Dengue Surveillance and Intervention Coordinator  
**Generated At**: 2026-10-29  

---

## Quick Navigation
* [Step 0: Synthetic Surveillance Data](#step-0-synthetic-surveillance-data)
* [Module 1: Spatial Graph Search & CSP](#module-1-spatial-graph-search--csp)
* [Module 2: Classical STRIPS / PDDL Planning](#module-2-classical-strips--pddl-planning)
* [Module 3: Bayesian Reasoning Under Uncertainty](#module-3-bayesian-reasoning-under-uncertainty)
* [Module 4: Reinforcement Learning (Q-Learning)](#module-4-reinforcement-learning-q-learning)
* [Module 5: Generative AI Multi-Agent Coordinator](#module-5-generative-ai-multi-agent-coordinator)
* [Automated Test Suite (pytest)](#automated-test-suite-pytest)

---

## Step 0: Synthetic Surveillance Data
* File: `data/districts_mock.csv` (10 urban districts, spatial adjacency topology, hospital bed counts)
* File: `data/weather_timeseries.csv` (14-day rainfall, temperature, and ovitrap counts)

---


## Module 1: Spatial Graph Search & CSP

### 1. Graph Search & Spatial Clustering
* **Total Nodes (Districts)**: 10
* **Total Edges (Adjacencies)**: 15
* **BFS Outbreak Cluster from D02 (Riverside Slums)**:
  `['D02', 'D04', 'D08', 'D10']`
* **Shortest Intervention Route (Dijkstra) from Depot D01 to Outbreak D10**:
  `D01 -> D02 -> D06 -> D10`

### 2. CSP Resource Allocation Solver
* **Test Scenario A: Feasible Budget ($10,000, Max Teams = 8)**
  * Total Feasible Allocations Found: **43**
  * Sample Optimal Allocation:
    * `D01` (Low Risk, 34 cases): 0 teams
    * `D02` (High Risk, 112 cases): **2 teams**
    * `D03` (Low Risk, 18 cases): 0 teams
    * `D04` (High Risk, 145 cases): **2 teams**
    * `D05` (Low Risk, 12 cases): 0 teams
    * `D06` (Low Risk, 22 cases): 0 teams
    * `D07` (Low Risk, 67 cases): 0 teams
    * `D08` (High Risk, 89 cases): **2 teams**
    * `D09` (Low Risk, 41 cases): 0 teams
    * `D10` (High Risk, 76 cases): **2 teams**
  * **Summary**: 8 teams deployed, $9,000 / $10,000 budget utilized.
* **Test Scenario B: Constraint Failure Demonstration ($1,000 Budget)**
  * Feasible Solutions: **0**
  * Result: `[OK] PASS`: Solver mathematically proves **UNSATISFIABLE** when resources cannot meet mandatory minimum risk constraints.

---

## Module 2: Classical STRIPS / PDDL Planning

### 1. Progression State-Space Planner
* **Initial State**: `[At(Team_Alpha, D01), Adjacent(D01, D02), Uninspected(D02)]`
* **Goal State**: `[Safe(D02)]`
* **Optimal 5-Step Plan Generated**:
  1. `Move(Team_Alpha, D01, D02)`
  2. `InspectBreedingSites(Team_Alpha, D02)`
  3. `SprayLarvicide(Team_Alpha, D02)`
  4. `DeployMedicalTreatment(Team_Alpha, D02)`
  5. `CertifyZoneSafe(HQ, D02)`
* Goal satisfied: **True**

### 2. Precondition Failure Test
* Attempting to spray when road is severed (no adjacency link) and site uninspected.
* Result: `[OK] PASS`: Planner detects **UNREACHABLE** state without violating domain preconditions.

---

## Module 3: Bayesian Reasoning Under Uncertainty

### 1. DAG Topology
* `Rainfall -> Mosquito_Density`
* `Mosquito_Density -> Dengue_Risk`
* `Human_Mobility -> Dengue_Risk`

### 2. Exact Inference (Variable Elimination)
1. **Prior Unconditional Risk**:
   $$P(\text{Dengue\_Risk}=\text{High}) = 0.4125$$
2. **Forward Causal Query (Rain Evidence)**:
   $$P(\text{Dengue\_Risk}=\text{High} \mid \text{Rainfall}=\text{High}) = 0.6562$$
3. **Compounding Threat Query (Rain + Mobility Evidence)**:
   $$P(\text{Dengue\_Risk}=\text{High} \mid \text{Rain}=\text{High}, \text{Mobility}=\text{High}) = 0.7950$$
4. **Diagnostic / Explaining Away Query**:
   $$P(\text{Rainfall}=\text{High} \mid \text{Dengue\_Risk}=\text{High}) = 0.6364$$
* Result: `[OK] PASS`: Posterior probabilities mathematically update monotonically under compounding risk.

---

## Module 4: Reinforcement Learning (Q-Learning)

### 1. Empirical Reward Convergence (800 Episodes)
| Episode Window | Mean Reward | Exploration Epsilon ($\epsilon$) |
|---|---|---|
| Episodes 1–100 | **-1.70** | 0.606 |
| Episodes 101–200 | **+100.45** | 0.367 |
| Episodes 201–300 | **+162.80** | 0.222 |
| Episodes 301–400 | **+195.25** | 0.135 |
| Episodes 401–500 | **+226.50** | 0.082 |
| Episodes 501–600 | **+230.40** | 0.050 |
| Episodes 601–700 | **+235.55** | 0.050 |
| Episodes 701–800 | **+238.95** | 0.050 |

* **Initial Mean**: $-1.70$
* **Final Mean**: $+238.95$
* **Performance Gain**: **+240.65 reward units**
* Result: `[OK] PASS`: Agent converged to high-reward policy.

### 2. Sample Learned Q-Table Policies
* State `(Zone=1, Risk=High, Chem=3)`: Action `1:SprayIntensive` (Q = 198.94)
* State `(Zone=1, Risk=High, Chem=0)`: Action `0:Move` (Refills/avoids futile spray)
* State `(Zone=0, Risk=Low, Chem=2)`: Action `2:FogContainment` (Conserves chemical)

---

## Module 5: Generative AI Multi-Agent Coordinator

### Agent 1: Central Surveillance Coordinator Directive
> **CODE RED**: Active outbreak clusters in Riverside Slums (D02), East Marshlands (D04), Harbor Area (D10).  
> Posterior Outbreak Probability: **0.80**.  
> CSP Allocations: **8 teams deployed**.  
> Directives: Mobilize barrier fogging, activate hydration wards, community inspection.

### Agent 2: Tactical Field Operations Commander
> **SQUAD ASSIGNMENT**: Unit Alpha-1 & Bravo-2 to Riverside Slums.  
> **EQUIPMENT**: ULV Cold Foggers, Bacillus thuringiensis israelensis (BTI).  
> **CHECKLIST**: N95 PPE, storm drain focus, 1g/1000L dosage, 30-min indoor shelter alert.

### Agent 3: Public Health Communications Advisory
> **COMMUNITY NOTICE**: High-risk epidemic notice issued for Riverside Slums.  
> **ACTIONS**: Eliminate stagnant water, apply DEET/Picaridin, close screen meshes.  
> **HOTLINE**: 1800-STOP-DENGUE with free NS1 antigen testing at Community Health Center.

---

## Automated Test Suite (pytest)
* Command: `pytest Dengue-Intervention/tests/`
* Result: **6 passed in 4.09s (100%)**

