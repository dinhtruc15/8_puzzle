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

def and_or_search(state, goal):
    """Modified AND-OR search algorithm."""
    def search(state, visited, depth=0):
        if depth > 10:  # Limit recursion depth
            return [state]  

        if state == goal:
            return [state]

        visited.add(state)
        results = []

        for child in get_children(state):
            print(f"Exploring: {child}")  # Show intermediate steps
            if child in visited:
                continue
            result = search(child, visited, depth + 1)
            if result:  # Append valid paths only
                results.append(result)

        visited.remove(state)

        if results:
            return [state] + results[0]  # Return the first valid path found
        else:
            return []  # Return an empty path if no valid paths are found

    visited = set()
    path = search(state, visited)

    # Final output handling
    if path:
        print("Path found:")
        for step in path:
            print(step)
    else:
        print("No solution found within depth limit.")
    return path

