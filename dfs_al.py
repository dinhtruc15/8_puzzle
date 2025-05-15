

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

def dfs(start, goal):
    """Iterative Deepening DFS with threshold heuristic."""
    def search(path, g, threshold, visited):
        state = path[-1]
        f = g + manhattan_distance(state, goal)
        if f > threshold:
            return f
        if state == goal:
            return path  # Solution found
        min_threshold = float('inf')
        for child in get_children(state):
            if child not in visited:
                visited.add(child)
                result = search(path + [child], g + 1, threshold, visited)
                if isinstance(result, list):  # Solution found
                    return result
                min_threshold = min(min_threshold, result)
                visited.remove(child)  # Allow revisiting with a different path
        return min_threshold

    threshold = manhattan_distance(start, goal)
    while True:
        visited = set([start])
        result = search([start], 0, threshold, visited)
        if isinstance(result, list):
            return result  # Solution found
        elif result == float('inf'):
            return None  # No solution possible
        threshold = result  # Update threshold
if __name__ == "__main__":
    print("dfs_al module is working correctly.")
