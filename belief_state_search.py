from collections import defaultdict

# Define possible moves
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_children(state):
    """Generate all possible child states from the current state."""
    children = []
    zero_idx = state.index(0)
    row, col = zero_idx // 3, zero_idx % 3

    for move in MOVES:
        new_row, new_col = row + move[0], col + move[1]
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_idx = new_row * 3 + new_col
            new_state = list(state)
            new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
            children.append(tuple(new_state))
    return children

def manhattan_distance(state, goal):
    """Calculate the Manhattan distance heuristic."""
    distance = 0
    for i, tile in enumerate(state):
        if tile == 0:  # Skip the empty tile
            continue
        goal_idx = goal.index(tile)
        distance += abs(goal_idx // 3 - i // 3) + abs(goal_idx % 3 - i % 3)
    return distance

def belief_state_search(initial_belief, goal, top_k=None, max_steps=100):
     #"""Optimized Belief State Search with adjusted exploration."""
    def generate_belief_states(belief_state):
     #"""Generate new belief states and sort heuristically."""
     new_belief = set()
     for state in belief_state:
        children = get_children(state)
        # Heuristic sorting (if top_k is specified)
        if top_k:
            children.sort(key=lambda x: manhattan_distance(x, goal))
            children = children[:top_k]
        for child in children:
            if child not in visited_all:
                new_belief.add(child)
                if child not in parent_map:
                    parent_map[child] = state
     return new_belief


    def goal_test(belief_state):
        return next((state for state in belief_state if state == goal), None)

    belief_state = set(initial_belief)
    visited_all = set(initial_belief)
    parent_map = {}
    steps = 0

    while belief_state and steps < max_steps:
        print(f"Step {steps}: Belief state size = {len(belief_state)}")
        
        goal_found = goal_test(belief_state)
        if goal_found:
            print(f"Goal reached in belief state at step {steps}")
            path = [goal_found]
            while path[-1] in parent_map:
                path.append(parent_map[path[-1]])
            path.reverse()
            return path

        next_belief_state = generate_belief_states(belief_state)
        next_belief_state = set(state for state in next_belief_state if state not in visited_all)

        if not next_belief_state:
            print("No solution found within the belief state space.")
            return None

        visited_all.update(next_belief_state)
        belief_state = next_belief_state
        steps += 1

    print("No solution found (step limit reached).")
    return None
