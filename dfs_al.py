

# Possible moves: up, down, left, right
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

def dfs(start, goal, max_depth=30):
    stack = [(start, [start])]
    while stack:
        state, path = stack.pop()
        if len(path) > max_depth:
            continue
        if state == goal:
            return path
        for child in get_children(state):
            if child not in path:
                stack.append((child, path + [child]))
    return None

