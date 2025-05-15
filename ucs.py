import heapq

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

def ucs(start, goal):
    """Uniform Cost Search (UCS) cho bài toán 8-Puzzle."""
    queue = [(0, start, [start])]  # (cost, state, path)
    visited = set()

    while queue:
        cost, state, path = heapq.heappop(queue)
        if state == goal:
            return path
        if state not in visited:
            visited.add(state)
            for child in get_children(state):
                if child not in visited:
                    heapq.heappush(queue, (cost + 1, child, path + [child]))
    return None
