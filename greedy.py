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

def manhattan_distance(state, goal):
    """Calculate the Manhattan distance heuristic for Greedy Search."""
    distance = 0
    for i in range(9):
        if state[i] == 0:
            continue
        goal_index = goal.index(state[i])
        goal_row, goal_col = goal_index // 3, goal_index % 3
        curr_row, curr_col = i // 3, i % 3
        distance += abs(goal_row - curr_row) + abs(goal_col - curr_col)
    return distance

def greedy_search(start, goal):
    """Greedy Search implementation for the 8-puzzle using Manhattan distance."""
    queue = [(manhattan_distance(start, goal), start, [start])]  # (heuristic, state, path)
    visited = {start}
    
    while queue:
        _, state, path = heapq.heappop(queue)
        if state == goal:
            return path  # Trả về danh sách trạng thái từ đầu đến đích
        
        for child in get_children(state):
            if child not in visited:
                visited.add(child)
                heapq.heappush(queue, (manhattan_distance(child, goal), child, path + [child]))
    
    return None  # Trả về None nếu không tìm thấy lời giải
