import heapq

class BeamSearch:
    def heuristic(self, state, goal_state):
       """Hàm heuristic: Kết hợp Manhattan distance và Linear Conflict"""
       distance = 0
       size = int(len(state) ** 0.5)  # Kích thước bảng (3x3)

       for i in range(len(state)):
          if state[i] != 0:
            goal_index = goal_state.index(state[i])
            row1, col1 = i // size, i % size
            row2, col2 = goal_index // size, goal_index % size
            distance += abs(row1 - row2) + abs(col1 - col2)

            # Tính toán Linear Conflict
            if row1 == row2:  # Cùng hàng
                for j in range(col1 + 1, size):
                    if state[row1 * size + j] != 0 and goal_state.index(state[row1 * size + j]) // size == row1:
                        if goal_state.index(state[row1 * size + j]) < goal_index:
                            distance += 2
            if col1 == col2:  # Cùng cột
                for j in range(row1 + 1, size):
                    if state[j * size + col1] != 0 and goal_state.index(state[j * size + col1]) % size == col1:
                        if goal_state.index(state[j * size + col1]) < goal_index:
                            distance += 2

       return distance


    def generate_neighbors(self, state):
        """Sinh ra các trạng thái hàng xóm bằng cách di chuyển ô trống"""
        neighbors = []
        zero_index = state.index(0)
        row, col = zero_index // 3, zero_index % 3
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, Xuống, Trái, Phải

        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_state = list(state)
                new_index = new_row * 3 + new_col
                new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
                neighbors.append(tuple(new_state))

        return neighbors

    def is_solvable(self, state):
        """Kiểm tra trạng thái có giải được không (tính số nghịch thế)"""
        inv_count = 0
        array = [x for x in state if x != 0]
        for i in range(len(array)):
            for j in range(i + 1, len(array)):
                if array[i] > array[j]:
                    inv_count += 1
        return inv_count % 2 == 0

    def solve(self, initial_state, goal_state, beam_width=3):
        """Giải bài toán 8-Puzzle bằng Beam Search"""
        if not self.is_solvable(initial_state):
            print("Trạng thái ban đầu không có lời giải!")
            return None

        current_state = tuple(initial_state)
        path = [current_state]
        visited = set()
        visited.add(current_state)

        # Beam chứa các cặp (độ ưu tiên, trạng thái, đường đi)
        beam = [(self.heuristic(current_state, goal_state), current_state, path)]

        while beam:
            # Lấy ra các trạng thái từ chùm
            next_beam = []
            for _, state, path in beam:
                # Kiểm tra nếu đã đạt được trạng thái đích
                if state == tuple(goal_state):
                    return path

                # Sinh ra hàng xóm và thêm vào beam
                neighbors = self.generate_neighbors(state)
                for neighbor in neighbors:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        new_path = path + [neighbor]
                        priority = self.heuristic(neighbor, goal_state)
                        heapq.heappush(next_beam, (priority, neighbor, new_path))

            # Chỉ giữ lại beam_width trạng thái tốt nhất
            beam = heapq.nsmallest(beam_width, next_beam)

        print("Không tìm được lời giải.")
        return None


