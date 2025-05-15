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

def softmax(Q_values, beta=1.0):
    Q_values = np.array(Q_values)
    Q_values = Q_values - np.max(Q_values)
    exp_values = np.exp(beta * Q_values)
    probabilities = exp_values / np.sum(exp_values)
    return np.random.choice(len(Q_values), p=probabilities)

def q_learning(start, goal, episodes=10000, alpha=0.1, gamma=0.99, epsilon=0.3):
    q_table = defaultdict(lambda: [0.0] * 4)
    start = tuple(start)
    goal = tuple(goal)

    for episode in range(episodes):
        state = start
        visited = set()
        state_str = state_to_str(state)

        for step in range(100):
            children = get_children_with_action(state)
            valid_actions = [a for (_, a) in children]
            if not valid_actions:
                break

            if random.random() < epsilon:
                action = random.choice(valid_actions)
            else:
                q_values = [q_table[state_str][a] if a in valid_actions else -np.inf for a in range(4)]
                action = softmax(q_values)

            next_state = [s for (s, a) in children if a == action][0]
            next_str = state_to_str(next_state)

            reward = 100 if next_state == goal else -1 - manhattan_distance(next_state, goal) / 10.0

            next_q_values = [q_table[next_str][a] for (s, a) in get_children_with_action(next_state)]
            max_next_q = max(next_q_values) if next_q_values else 0
            q_table[state_str][action] += alpha * (reward + gamma * max_next_q - q_table[state_str][action])

            state = next_state
            state_str = next_str

            if state == goal or state_str in visited:
                break
            visited.add(state_str)

        epsilon = max(0.01, epsilon * 0.995)

    # Reconstruct path
    state = start
    path = [list(state)]
    visited = set([state_to_str(state)])

    for _ in range(100):
        state_str = state_to_str(state)
        if state_str not in q_table:
            return None

        children = get_children_with_action(state)
        valid_actions = [a for (_, a) in children]
        if not valid_actions:
            return None
        q_values = [q_table[state_str][a] if a in valid_actions else -np.inf for a in range(4)]
        action = np.argmax(q_values)

        next_states = [s for (s, a) in children if a == action]
        if not next_states:
            return None
        state = next_states[0]
        state_str = state_to_str(state)

        if state_str in visited:
            return None
        visited.add(state_str)

        path.append(list(state))
        if state == goal:
            return path

    return None

# === Example usage ===
if __name__ == "__main__":
    start_state = [1, 2, 3, 4, 5, 6, 0, 7, 8]  # bạn có thể thay bằng ví dụ khác
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    
    path = q_learning(start_state, goal_state)
    
    if path:
        print("✅ Path found:")
        for step, state in enumerate(path):
            print(f"Bước {step+1}:")
            print(state[:3])
            print(state[3:6])
            print(state[6:])
            print()
    else:
        print("❌ Không tìm thấy lời giải.")
