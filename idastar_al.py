import heapq
def manhattan_distance(state, goal):
    """Tính tổng khoảng cách Manhattan giữa các ô hiện tại và trạng thái mục tiêu"""
    distance = 0
    for num in range(1, 9):  # Không tính ô trống (0)
        x1, y1 = divmod(state.index(num), 3)  # Vị trí số trong trạng thái hiện tại
        x2, y2 = divmod(goal.index(num), 3)   # Vị trí số trong trạng thái mục tiêu
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

def ida_star(initial_state, goal_state):
    def search(path, g, threshold, visited):
        state = path[-1]
        f = g + manhattan_distance(state, goal_state)
        
        if f > threshold:
            return f  # Trả về giá trị ngưỡng mới
        
        if state == goal_state:
            return path
        
        min_threshold = float("inf")
        zero_index = state.index(0)
        row, col = divmod(zero_index, 3)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_index = new_row * 3 + new_col
                new_state = list(state)
                new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
                new_state = tuple(new_state)

                if new_state not in visited:
                    visited.add(new_state)
                    result = search(path + [new_state], g + 1, threshold, visited)
                    if isinstance(result, list):
                        return result  # Tìm thấy lời giải
                    min_threshold = min(min_threshold, result)
                    visited.remove(new_state)

        return min_threshold

    threshold = manhattan_distance(initial_state, goal_state) + 15
    while True:
      visited = set([initial_state])
      result = search([initial_state], 0, threshold, visited)

      if isinstance(result, list):  
          return result  # Đã tìm thấy lời giải, trả về danh sách các bước đi
      elif isinstance(result, int):
          threshold = result + 1  # Cập nhật threshold chậm hơn
      else:
         return None  # Không tìm thấy lời giải


