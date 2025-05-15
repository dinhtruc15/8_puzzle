import random

MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

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

def manhattan_distance(state):
    """Đánh giá trạng thái dựa trên khoảng cách Manhattan."""
    distance = 0
    for i in range(9):
        if state[i] != 0:
            goal_pos = GOAL_STATE.index(state[i])
            cur_row, cur_col = divmod(i, 3)
            goal_row, goal_col = divmod(goal_pos, 3)
            distance += abs(cur_row - goal_row) + abs(cur_col - goal_col)
    return distance

def crossover(p1, p2):
    """Ghép hai cha mẹ theo kiểu cắt điểm."""
    cut = random.randint(1, 7)
    child = list(p1[:cut])
    for gene in p2:
        if gene not in child:
            child.append(gene)
    return tuple(child)

def mutate(state, mutation_rate=0.2):
    """Hoán đổi ngẫu nhiên hai vị trí để tạo đột biến."""
    state = list(state)
    if random.random() < mutation_rate:
        i, j = random.sample(range(9), 2)
        state[i], state[j] = state[j], state[i]
    return tuple(state)
def is_solvable(state):
    """Kiểm tra xem trạng thái có thể giải được hay không, dựa trên số lần đảo vị."""
    inv = 0
    flat_state = [num for num in state if num != 0]  # Bỏ số 0 để xét thứ tự nghịch đảo
    
    for i in range(len(flat_state)):
        for j in range(i + 1, len(flat_state)):
            if flat_state[i] > flat_state[j]:  # Đếm số lần một số lớn hơn xuất hiện trước số nhỏ hơn
                inv += 1

    return inv % 2 == 0  # Nếu số nghịch đảo là chẵn, trạng thái có thể giải được

def genetic(start, goal=GOAL_STATE, population_size=100, generations=500):
    if not is_solvable(start):
        return None

    population = [(start, [start])]  # Thêm đường đi vào mỗi cá thể
    while len(population) < population_size:
        state = tuple(random.sample(range(9), 9))
        population.append((state, [state]))

    for generation in range(generations):
        population.sort(key=lambda x: manhattan_distance(x[0]))  # Sắp xếp dựa trên heuristic

        if population[0][0] == goal:
            print(f"Tìm thấy lời giải sau {generation} thế hệ!")
            return population[0][1]

        # Chọn top N cá thể tốt nhất làm cha mẹ
        parents = population[:20]
        next_generation = parents[:2]  # Giữ lại elite

        while len(next_generation) < population_size:
            p1, p2 = random.sample(parents, 2)
            child_state = mutate(crossover(p1[0], p2[0]))
            child_path = p1[1] + [child_state]  # Theo dõi đường đi
            next_generation.append((child_state, child_path))

        population = next_generation

    print("Không tìm thấy lời giải trong giới hạn thế hệ.")
    return None
