def get_children(state):
    children = []
    zero_idx = state.index(0)
    row, col = zero_idx // 3, zero_idx % 3

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_idx = new_row * 3 + new_col
            new_state = list(state)
            new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
            children.append(tuple(new_state))
    return children

def backtracking_with_forward_checking(state, goal, path=None, visited=None, max_depth=30):
    if path is None:
        path = [state]
    if visited is None:
        visited = set()

    if state == goal:
        return path
    if len(path) > max_depth:
        return None

    visited.add(state)

    for child in get_children(state):
        if child not in visited:
            new_path = backtracking_with_forward_checking(child, goal, path + [child], visited, max_depth)
            if new_path:
                return new_path

    return None
