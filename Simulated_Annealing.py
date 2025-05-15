import math
import random

class SimulatedAnnealing:
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

    def probability(self, delta_e, temperature):
        """Tính xác suất chấp nhận trạng thái tệ hơn"""
        return math.exp(-delta_e / temperature)

    def solve(self, initial_state, goal_state, initial_temp=1000, cooling_rate=0.99, min_temp=0.1):
        """Giải bài toán 8-Puzzle bằng Simulated Annealing"""
        current_state = tuple(initial_state)
        current_h = self.heuristic(current_state, goal_state)
        path = [current_state]
        temperature = initial_temp

        while temperature > min_temp:
            if current_state == tuple(goal_state):
                return path

            neighbors = self.generate_neighbors(current_state)
            next_state = random.choice(neighbors)
            next_h = self.heuristic(next_state, goal_state)
            delta_e = next_h - current_h

            # Chấp nhận trạng thái mới nếu tốt hơn hoặc theo xác suất
            if delta_e < 0 or random.random() < self.probability(delta_e, temperature):
                current_state = next_state
                current_h = next_h
                path.append(current_state)

            # Giảm nhiệt độ
            temperature *= cooling_rate

        return path

    