import random
import numpy as np
from collections import defaultdict

MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]
ACTIONS = ['up', 'down', 'left', 'right']

def get_children_with_action(state):
    children = []
    zero_idx = state.index(0)
    row, col = divmod(zero_idx, 3)

    for idx, (dr, dc) in enumerate(MOVES):
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_idx = new_row * 3 + new_col
            new_state = list(state)
            new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
            children.append((tuple(new_state), idx))
    return children

def state_to_str(state):
    return ''.join(map(str, state))

def manhattan_distance(state, goal):
    distance = 0
    for i in range(9):
        if state[i] != 0:
            goal_pos = goal.index(state[i])
            row, col = divmod(i, 3)
            goal_row, goal_col = divmod(goal_pos, 3)
            distance += abs(row - goal_row) + abs(col - goal_col)
    return distance

def choose_action(state_str, q_table, valid_actions, epsilon):
    if random.random() < epsilon:
        return random.choice(valid_actions)
    q_values = [q_table[state_str][a] if a in valid_actions else -np.inf for a in range(4)]
    return int(np.argmax(q_values))

def sarsa(start, goal, episodes=5000, alpha=0.1, gamma=0.99, epsilon=0.3):
    q_table = defaultdict(lambda: [0.0] * 4)
    goal = tuple(goal)
    start = tuple(start)

    for episode in range(episodes):
        state = start
        state_str = state_to_str(state)
        visited = set()
        children = get_children_with_action(state)
        valid_actions = [a for (_, a) in children]
        action = choose_action(state_str, q_table, valid_actions, epsilon)

        for _ in range(100):  # step limit
            next_state = [s for (s, a) in children if a == action][0]
            next_str = state_to_str(next_state)
            next_children = get_children_with_action(next_state)
            next_valid_actions = [a for (_, a) in next_children]
            next_action = choose_action(next_str, q_table, next_valid_actions, epsilon)

            # Reward
            if next_state == goal:
                reward = 100
            else:
                reward = -1 - manhattan_distance(next_state, goal) / 10.0

            # Update Q-value
            q_table[state_str][action] += alpha * (
                reward + gamma * q_table[next_str][next_action] - q_table[state_str][action]
            )

            if next_state == goal:
                break

            state = next_state
            state_str = next_str
            children = next_children
            action = next_action

        # Epsilon decay
        epsilon = max(0.01, epsilon * 0.995)

    # Reconstruct path
    state = start
    path = [list(state)]
    visited = set([state_to_str(state)])

    for _ in range(100):
        state_str = state_to_str(state)
        children = get_children_with_action(state)
        valid_actions = [a for (_, a) in children]
        q_values = [q_table[state_str][a] if a in valid_actions else -np.inf for a in range(4)]
        action = int(np.argmax(q_values))
        next_states = [s for (s, a) in children if a == action]
        if not next_states:
            return None
        state = next_states[0]
        if state_to_str(state) in visited:
            return None
        visited.add(state_to_str(state))
        path.append(list(state))
        if state == goal:
            return path
    return None
