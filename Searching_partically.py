from collections import deque

MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_children(state):
    children = []
    zero_idx = state.index(0)
    row, col = divmod(zero_idx, 3)

    for dr, dc in MOVES:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_idx = new_row * 3 + new_col
            new_state = list(state)
            new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
            children.append(tuple(new_state))
    return children

def searching_partically(start, goal):
    queue = deque([(start, [start])])
    visited = set([start])  # Khởi đầu đã được thăm

    while queue:
        state, path = queue.popleft()
        if state == goal:
            return path

        for child in get_children(state):
            if child not in visited:
                visited.add(child)
                queue.append((child, path + [child]))

    return None

