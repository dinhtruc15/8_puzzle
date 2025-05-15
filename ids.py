from collections import deque

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

def dls(state, goal, path, depth, visited):
    """Depth-Limited Search (DLS) dùng trong IDS."""
    if state == goal:
        return path
    if depth <= 0:
        return None
    for child in get_children(state):
        if child not in visited:
            visited.add(child)
            result = dls(child, goal, path + [child], depth - 1, visited)
            if result:
                return result
    return None

def ids(start, goal):
    """Iterative Deepening Search (IDS) cho bài toán 8-Puzzle."""
    depth = 0
    while True:
        visited = {start}
        result = dls(start, goal, [start], depth, visited)
        if result:
            return result
        depth += 1
