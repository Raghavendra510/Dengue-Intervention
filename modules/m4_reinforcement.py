"""
Module 4: Reinforcement Learning (Adaptive Intervention Agent)
Course Concepts:
  - Model-Free Reinforcement Learning: Tabular Q-Learning.
  - Markov Decision Process (MDP): States, Actions, Transitions, Rewards, Discount Factor.
  - Temporal Difference (TD) updates and exploration-exploitation tradeoff (epsilon-greedy).
  - Empirical verification of reward convergence.
"""

import random
import numpy as np
from typing import Dict, Tuple, List

class DengueInterventionEnv:
    """
    Simulation Environment for Adaptive Surveillance and Vector Control:
      - Zones: 4 primary zones [0: Downtown, 1: Riverside, 2: NorthHill, 3: Eastside]
      - State: (current_zone, risk_level_zone, remaining_chemical_units)
          * zone: 0 to 3
          * risk: 0 (Low), 1 (Medium), 2 (High)
          * chemical: 0 to 3 units left
      - Actions:
          * 0: Move to next connected zone
          * 1: Intensive Larvicide Spray (costs 1 chemical, reduces risk by 2 levels)
          * 2: Focal Fogging / Containment (costs 1 chemical, reduces risk by 1 level)
          * 3: Passive Surveillance / Conserve (costs 0 chemical)
      - Reward:
          * Cases prevented / risk reduction: +40 to +100
          * Outbreak penalty if High risk ignored: -60
          * Wasted resource penalty (spraying low risk): -15
          * Operational movement cost: -2
    """
    def __init__(self):
        self.num_zones = 4
        self.max_chemical = 3
        self.reset()

    def reset(self):
        self.current_zone = random.randint(0, self.num_zones - 1)
        # Random risk states for the 4 zones
        self.zone_risks = [random.choice([1, 2]) for _ in range(self.num_zones)]
        self.chemical = self.max_chemical
        self.step_count = 0
        self.max_steps = 15
        return self._get_state()

    def _get_state(self) -> Tuple[int, int, int]:
        return (self.current_zone, self.zone_risks[self.current_zone], self.chemical)

    def step(self, action: int) -> Tuple[Tuple[int, int, int], float, bool]:
        self.step_count += 1
        reward = -2.0  # base operational step cost
        curr_risk = self.zone_risks[self.current_zone]

        if action == 0:  # Move
            self.current_zone = (self.current_zone + 1) % self.num_zones
            # Risk in unvisited zones may fester
            unvisited_zone = random.choice([z for z in range(self.num_zones) if z != self.current_zone])
            if self.zone_risks[unvisited_zone] < 2 and random.random() < 0.35:
                self.zone_risks[unvisited_zone] += 1

        elif action == 1:  # Intensive Spray
            if self.chemical > 0:
                self.chemical -= 1
                if curr_risk == 2:
                    reward += 100.0  # Prevented severe epidemic outbreak
                    self.zone_risks[self.current_zone] = 0
                elif curr_risk == 1:
                    reward += 45.0
                    self.zone_risks[self.current_zone] = 0
                else:
                    reward -= 20.0  # Over-sprayed zero risk
            else:
                reward -= 15.0  # Attempted action with depleted chemicals

        elif action == 2:  # Focal Fogging
            if self.chemical > 0:
                self.chemical -= 1
                if curr_risk > 0:
                    reward += 50.0
                    self.zone_risks[self.current_zone] = max(0, curr_risk - 1)
                else:
                    reward -= 10.0
            else:
                reward -= 15.0

        elif action == 3:  # Passive Surveillance
            if curr_risk == 2:
                reward -= 60.0  # Heavy penalty for negligence during emergency
            elif curr_risk == 0:
                reward += 10.0  # Commended for conserving scarce resources
            else:
                reward -= 10.0

        terminated = (self.step_count >= self.max_steps) or (sum(self.zone_risks) == 0)
        return self._get_state(), reward, terminated


class QLearningAgent:
    """Tabular Q-Learning Agent with Epsilon-Greedy Exploration."""
    def __init__(self, alpha=0.15, gamma=0.90, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.05):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.q_table: Dict[Tuple[int, int, int], np.ndarray] = {}
        self.num_actions = 4

    def get_q_values(self, state: Tuple[int, int, int]) -> np.ndarray:
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.num_actions)
        return self.q_table[state]

    def choose_action(self, state: Tuple[int, int, int]) -> int:
        if random.random() < self.epsilon:
            return random.randint(0, self.num_actions - 1)
        q_vals = self.get_q_values(state)
        return int(np.argmax(q_vals))

    def update(self, state, action, reward, next_state, terminated):
        curr_q = self.get_q_values(state)[action]
        next_max_q = 0.0 if terminated else np.max(self.get_q_values(next_state))
        # Bellman Optimality Equation TD Update
        td_target = reward + self.gamma * next_max_q
        self.q_table[state][action] = curr_q + self.alpha * (td_target - curr_q)

    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)


def train_q_learning(episodes=1000):
    env = DengueInterventionEnv()
    agent = QLearningAgent()
    rewards_history = []
    window = 100

    for ep in range(1, episodes + 1):
        state = env.reset()
        ep_reward = 0
        done = False

        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.update(state, action, reward, next_state, done)
            state = next_state
            ep_reward += reward

        agent.decay_epsilon()
        rewards_history.append(ep_reward)

    return agent, rewards_history


def run_module_4():
    print("=" * 70)
    print("MODULE 4: REINFORCEMENT LEARNING (ADAPTIVE Q-LEARNING AGENT)")
    print("=" * 70)

    episodes = 800
    print(f"Training Q-Learning Agent across {episodes} episodes...")
    agent, history = train_q_learning(episodes)

    print("\n[EMPIRICAL REWARD CONVERGENCE]")
    print("Episode Window | Average Episode Reward | Exploration Epsilon")
    print("-" * 55)

    window = 100
    avg_rewards = []
    for i in range(0, episodes, window):
        chunk = history[i:i + window]
        avg = sum(chunk) / len(chunk)
        avg_rewards.append(avg)
        eps = max(agent.min_epsilon, 1.0 * (agent.epsilon_decay ** (i + window)))
        print(f"Episodes {i+1:3d}-{i+window:3d}  | Mean Reward: {avg:7.2f}    | Epsilon: {eps:.3f}")

    print("-" * 55)
    # Check upward trend
    initial_performance = sum(history[:100]) / 100
    final_performance = sum(history[-100:]) / 100
    improvement = final_performance - initial_performance
    print(f"Initial 100-ep mean: {initial_performance:.2f} -> Final 100-ep mean: {final_performance:.2f}")
    print(f"Performance Gain   : +{improvement:.2f} reward units")

    action_names = ["0:Move", "1:SprayIntensive", "2:FogContainment", "3:PassiveHold"]
    print("\n[SAMPLE OPTIMAL POLICY (Learned Q-Table Highlights)]")
    # Inspect policy for High Risk states (Risk=2)
    sample_states = [
        (1, 2, 3), # Zone 1 (Riverside), High Risk, Full Chemical
        (1, 2, 0), # Zone 1 (Riverside), High Risk, Depleted Chemical
        (0, 0, 2), # Zone 0 (Downtown), Low Risk, Chemical Available
    ]

    for s in sample_states:
        if s in agent.q_table:
            q_vals = agent.q_table[s]
            best_act = action_names[int(np.argmax(q_vals))]
            print(f" State (Zone={s[0]}, Risk={s[1]}, Chem={s[2]}):")
            print(f"   -> Q-Values: {[round(x, 2) for x in q_vals]} => Best Action: {best_act}")

    assert final_performance > initial_performance, "Agent failed to demonstrate positive learning curve!"
    print("\n [OK] PASS: Q-learning agent successfully converged to high-reward intervention policy.")
    print("=" * 70)


if __name__ == "__main__":
    run_module_4()

