import heapq

def manhattan_distance(state, goal_state):
    """Tính toán khoảng cách Manhattan giữa trạng thái hiện tại và trạng thái mục tiêu."""
    distance = 0
    for i in range(9):
        if state[i] != 0:
            x1, y1 = divmod(state[i], 3)
            x2, y2 = divmod(goal_state.index(state[i]), 3)
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

def astar(initial_state, goal_state):
    """Thuật toán A* tìm đường đi tối ưu."""
    frontier = []
    heapq.heappush(frontier, (0, 0, initial_state, []))  # (f(n), g(n), state, path)
    visited = set()

    while frontier:
        _, g, state, path = heapq.heappop(frontier)

        if state == goal_state:
            return path + [state]

        if state in visited:
            continue
        visited.add(state)

        zero_index = state.index(0)
        row, col = divmod(zero_index, 3)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_index = new_row * 3 + new_col
                new_state = list(state)
                new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
                new_state = tuple(new_state)

                if new_state not in visited:
                    h = manhattan_distance(new_state, goal_state)
                    heapq.heappush(frontier, (g + 1 + h, g + 1, new_state, path + [state]))

    return None  # Không tìm thấy đường đi
