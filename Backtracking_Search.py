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

def Backtracking_Search(start, goal, max_depth=30):
    """Backtracking Search cho bài toán 8-Puzzle."""

    path = []
    visited = set()

    def dfs(state, depth):
        if state == goal:
            path.append(state)
            return True
        if depth >= max_depth:
            return False

        visited.add(state)

        for child in get_children(state):
            if child not in visited:
                if dfs(child, depth + 1):
                    path.append(state)
                    return True

        visited.remove(state)
        return False

    if dfs(start, 0):
        path.reverse()  # Đảo ngược để có đường đi từ start đến goal
        return path
    else:
        print("Không tìm thấy lời giải trong giới hạn độ sâu.")
        return None
