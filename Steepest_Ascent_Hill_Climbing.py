import random 

class SteepestAscentHillClimbing:
    def heuristic(self, state, goal_state):
        """Hàm heuristic: Đếm số ô sai vị trí"""
        return sum(1 for i in range(len(state)) if state[i] != goal_state[i] and state[i] != 0)

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

    def solve(self, initial_state, goal_state):
        """Giải bài toán 8-Puzzle bằng Steepest-Ascent Hill Climbing"""
        current_state = tuple(initial_state)
        current_h = self.heuristic(current_state, goal_state)
        path = [current_state]

        while True:
            if current_state == goal_state:
                return path

            neighbors = self.generate_neighbors(current_state)

            # Tìm trạng thái hàng xóm có heuristic nhỏ nhất (tốt nhất)
            best_neighbor = None
            best_h = float("inf")

            for neighbor in neighbors:
                h = self.heuristic(neighbor, goal_state)
                if h < best_h:
                    best_h = h
                    best_neighbor = neighbor

            # Nếu không có cải thiện, dừng lại
            if best_h >= current_h:
                return path

            # Cập nhật trạng thái hiện tại với hàng xóm tốt nhất
            current_state = best_neighbor
            current_h = best_h
            path.append(current_state)
