"""
Module 2: Classical Planning (STRIPS / PDDL Engine)
Course Concepts:
  - Classical Planning: State-space representation, Preconditions, Effects,
    and Forward Search (Progression Planning).
  - PDDL (Planning Domain Definition Language) semantics for vector control:
    Inspect -> Confirm Breeding Site -> Spray Larvicide -> Treat -> Certify Safe.
"""

import os
from collections import deque
from typing import List, Set, Tuple, Dict, Optional

class Action:
    def __init__(self, name: str, params: Tuple[str, ...], preconditions: Set[str], add_effects: Set[str], del_effects: Set[str]):
        self.name = name
        self.params = params
        self.preconditions = preconditions
        self.add_effects = add_effects
        self.del_effects = del_effects

    def is_applicable(self, state: Set[str]) -> bool:
        return self.preconditions.issubset(state)

    def apply(self, state: Set[str]) -> Set[str]:
        new_state = set(state)
        new_state.difference_update(self.del_effects)
        new_state.update(self.add_effects)
        return new_state

    def __repr__(self):
        return f"{self.name}({', '.join(self.params)})"


class ClassicalPlanner:
    """
    Forward State-Space Search (Progression Planning) for Dengue Intervention.
    Guarantees finding optimal sequential plans satisfying all PDDL action preconditions.
    """
    def __init__(self):
        self.actions: List[Action] = []

    def register_action(self, action: Action):
        self.actions.append(action)

    def plan(self, initial_state: Set[str], goal_state: Set[str]) -> Optional[List[Action]]:
        """Breadth-First Forward State-Space Search."""
        queue = deque([(initial_state, [])])
        visited = set()
        visited.add(frozenset(initial_state))

        while queue:
            curr_state, path = queue.popleft()

            # Check if goal predicates are satisfied
            if goal_state.issubset(curr_state):
                return path

            for action in self.actions:
                if action.is_applicable(curr_state):
                    next_state = action.apply(curr_state)
                    state_key = frozenset(next_state)
                    if state_key not in visited:
                        visited.add(state_key)
                        queue.append((next_state, path + [action]))
        return None


def setup_dengue_planning_domain(districts: List[str], adjacencies: List[Tuple[str, str]], teams: List[str]) -> ClassicalPlanner:
    planner = ClassicalPlanner()

    for team in teams:
        # Move action across adjacent districts
        for src, dst in adjacencies:
            planner.register_action(Action(
                name="Move",
                params=(team, src, dst),
                preconditions={f"At({team}, {src})", f"Adjacent({src}, {dst})"},
                add_effects={f"At({team}, {dst})"},
                del_effects={f"At({team}, {src})"}
            ))

        # Inspect zone
        for loc in districts:
            planner.register_action(Action(
                name="InspectBreedingSites",
                params=(team, loc),
                preconditions={f"At({team}, {loc})", f"Uninspected({loc})"},
                add_effects={f"Inspected({loc})", f"BreedingSiteConfirmed({loc})"},
                del_effects={f"Uninspected({loc})"}
            ))

        # Spray larvicide / fogging (Precondition: site must be confirmed)
        for loc in districts:
            planner.register_action(Action(
                name="SprayLarvicide",
                params=(team, loc),
                preconditions={f"At({team}, {loc})", f"BreedingSiteConfirmed({loc})"},
                add_effects={f"Sprayed({loc})"},
                del_effects=set()
            ))

        # Treat patients & setup hydration center
        for loc in districts:
            planner.register_action(Action(
                name="DeployMedicalTreatment",
                params=(team, loc),
                preconditions={f"At({team}, {loc})", f"Sprayed({loc})"},
                add_effects={f"CasesTreated({loc})"},
                del_effects=set()
            ))

    # Autonomous Certification: Once sprayed & treated, certify safe
    for loc in districts:
        planner.register_action(Action(
            name="CertifyZoneSafe",
            params=("HQ", loc),
            preconditions={f"Sprayed({loc})", f"CasesTreated({loc})"},
            add_effects={f"Safe({loc})"},
            del_effects=set()
        ))

    return planner


def run_module_2():
    print("=" * 70)
    print("MODULE 2: CLASSICAL PLANNING (PDDL / STRIPS STATE-SPACE SEARCH)")
    print("=" * 70)

    districts = ["D01", "D02", "D04"]
    adjacencies = [("D01", "D02"), ("D02", "D01"), ("D02", "D04"), ("D04", "D02")]
    teams = ["Team_Alpha"]

    planner = setup_dengue_planning_domain(districts, adjacencies, teams)

    print("\n[PLANNING PROBLEM DEFINITION]")
    init_state = {
        "At(Team_Alpha, D01)",
        "Adjacent(D01, D02)",
        "Adjacent(D02, D01)",
        "Adjacent(D02, D04)",
        "Adjacent(D04, D02)",
        "Uninspected(D02)"
    }
    goal_state = {"Safe(D02)"}

    print(f"Initial State : {sorted(list(init_state))}")
    print(f"Goal State    : {sorted(list(goal_state))}")

    print("\n[SOLVING SCENARIO 1: FEASIBLE INTERVENTION PIPELINE]")
    plan = planner.plan(init_state, goal_state)

    if plan:
        print(f" -> Optimal Plan Found ({len(plan)} sequential steps):")
        curr = set(init_state)
        for idx, act in enumerate(plan, 1):
            print(f"   Step {idx}: {act}")
            curr = act.apply(curr)
        print(f" -> Final State satisfies goal: {goal_state.issubset(curr)}")
    else:
        print(" -> No plan found!")

    print("\n[SOLVING SCENARIO 2: PRECONDITION VIOLATION / IMPOSSIBLE PLAN]")
    print("Test: Attempting to spray D04 when road is severed (No Adjacency) and Site Not Inspected")
    severed_init_state = {
        "At(Team_Alpha, D01)",
        # No adjacency between D01 and D04
        "Uninspected(D04)"
    }
    severed_goal = {"Safe(D04)"}
    failed_plan = planner.plan(severed_init_state, severed_goal)
    if failed_plan is None:
        print(" [OK] PASS: Planner correctly identified UNREACHABLE goal state due to unmet preconditions.")

    print("=" * 70)


if __name__ == "__main__":
    run_module_2()
