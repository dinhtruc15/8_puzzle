import time
import tkinter as tk
import heapq
from tkinter import ttk, messagebox
from bfs import bfs
from dfs_al import dfs
from ids import ids
from ucs import ucs
from greedy import greedy_search
from astar_al import astar
from idastar_al import ida_star
from hill_climbing import HillClimbing
from Steepest_Ascent_Hill_Climbing import SteepestAscentHillClimbing
from Stochastic_Hill_Climbing import StochasticHillClimbing
from Simulated_Annealing import SimulatedAnnealing
from Beam_Search import BeamSearch
from and_or_search import and_or_search
from belief_state_search import belief_state_search
from Backtracking_Search import Backtracking_Search
from Searching_partically import searching_partically
from GA import genetic
from Q_Learning_8p import q_learning
from Sarsa_8p import sarsa
from Backtracking_FC import backtracking_with_forward_checking

def parse_input(entries):
    try:
        values = [int(entry.get()) for row in entries for entry in row]
        if sorted(values) != list(range(9)):
            raise ValueError("Nhập các số từ 0 đến 8, không trùng nhau.")
        return tuple(values)
    except ValueError as e:
        messagebox.showerror("Lỗi nhập liệu", str(e))
        return None

class PuzzleGUI:
    def setup_entry_navigation(self, entries, next_entries=None):
        for i in range(3):
            for j in range(3):
                entry = entries[i][j]
                entry.bind("<Left>", lambda e, x=i, y=j: self.move_focus(entries, x, y, 0, -1))
                entry.bind("<Right>", lambda e, x=i, y=j: self.move_focus(entries, x, y, 0, 1))
                entry.bind("<Up>", lambda e, x=i, y=j: self.move_focus(entries, x, y, -1, 0))
                entry.bind("<Down>", lambda e, x=i, y=j: self.move_focus(entries, x, y, 1, 0))
                entry.bind("<Return>", lambda e, x=i, y=j: self.move_next_entry(entries, x, y, next_entries))

    def move_focus(self, entries, row, col, d_row, d_col):
        new_row = (row + d_row) % 3
        new_col = (col + d_col) % 3
        entries[new_row][new_col].focus_set()

    def move_next_entry(self, entries, row, col, next_entries=None):
        if col < 2:
            entries[row][col + 1].focus_set()
        elif row < 2:
            entries[row + 1][0].focus_set()
        elif next_entries:
            next_entries[0][0].focus_set()
        else:
            self.copy_initial_to_current()

    def __init__(self, root):
        self.root = root
        self.root.title("Solve 8-puzzle")
        self.root.state("zoomed")
        self.root.configure(bg="#e0f7fa")

        left_frame = tk.Frame(root, bg="#e0f7fa")
        left_frame.pack(side="left", padx=50, pady=20, expand=True, fill="both")

        control_frame = tk.Frame(left_frame, bg="#e0f7fa")
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Chọn thuật toán:", bg="#e0f7fa", font=("Arial", 14, "bold"), fg="#004d40").pack(anchor="w")
        self.algo_var = tk.StringVar(value="BFS")
        algorithms = ["BFS", "UCS", "DFS", "IDS", "Greedy Search", "A* Search", "IDA* Search", "Hill Climbing", "Steepest-Ascent Hill Climbing",
                      "Stochastic Hill Climbing", "Simulated Annealing", "Beam Search", 
                      "And-Or Search", "Belief State Search", "Backtracking Search", "Searching partically","GA",
                      "Q-Learning", "Sarsa", "Backtracking with Forward Checking"]
        self.algo_menu = ttk.Combobox(control_frame, textvariable=self.algo_var, values=algorithms, width=25, font=("Arial", 12))
        self.algo_menu.pack(anchor="w", pady=5)

        button_frame = tk.Frame(control_frame, bg="#e0f7fa")
        button_frame.pack(pady=10)

        self.solve_button = tk.Button(button_frame, text="Giải", command=self.solve_puzzle, font=("Arial", 12, "bold"),
                                      bg="#00796b", fg="white", activebackground="#004d40", activeforeground="white", width=10)
        self.solve_button.pack(side="left", padx=5)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_puzzle, font=("Arial", 12, "bold"),
                                      bg="#00796b", fg="white", activebackground="#004d40", activeforeground="white", width=10)
        self.reset_button.pack(side="left", padx=5)

        tk.Label(left_frame, text="Trạng thái ban đầu:", bg="#e0f7fa", font=("Arial", 14, "bold"), fg="#004d40").pack(anchor="w", pady=5)
        self.initial_entries = []
        for i in range(3):
            row_frame = tk.Frame(left_frame, bg="#e0f7fa")
            row_frame.pack()
            row = []
            for j in range(3):
                entry = tk.Entry(row_frame, width=5, font=("Arial", 18), justify="center",
                                 bg="white", fg="#004d40", highlightbackground="#80cbc4", highlightthickness=2)
                entry.pack(side="left", padx=2, pady=2)
                entry.insert(0, "")
                row.append(entry)
            self.initial_entries.append(row)

        tk.Label(left_frame, text="Trạng thái thực hiện:", bg="#e0f7fa", font=("Arial", 14, "bold"), fg="#004d40").pack(anchor="w", pady=5)
        self.current_entries = []
        for i in range(3):
            row_frame = tk.Frame(left_frame, bg="#e0f7fa")
            row_frame.pack()
            row = []
            for j in range(3):
                entry = tk.Entry(row_frame, width=5, font=("Arial", 18), justify="center",
                                 bg="white", fg="#004d40", highlightbackground="#80cbc4", highlightthickness=2)
                entry.pack(side="left", padx=2, pady=2)
                entry.insert(0, "")
                entry.config(state="readonly")
                row.append(entry)
            self.current_entries.append(row)

        tk.Label(left_frame, text="Trạng thái đích:", bg="#e0f7fa", font=("Arial", 14, "bold"), fg="#004d40").pack(anchor="w", pady=5)
        self.goal_entries = []
        for i in range(3):
            row_frame = tk.Frame(left_frame, bg="#e0f7fa")
            row_frame.pack()
            row = []
            for j in range(3):
                entry = tk.Entry(row_frame, width=5, font=("Arial", 18), justify="center",
                                 bg="white", fg="#004d40", highlightbackground="#80cbc4", highlightthickness=2)
                entry.pack(side="left", padx=2, pady=2)
                entry.insert(0, "")
                row.append(entry)
            self.goal_entries.append(row)

        right_frame = tk.Frame(root, bg="#e0f7fa")
        right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        result_frame = tk.Frame(right_frame, bg="#e0f7fa")
        result_frame.pack(fill="both", expand=True)

        self.move_label = tk.Label(result_frame, text="Bước hiện tại: ", bg="#e0f7fa", fg="#004d40", font=("Arial", 14, "bold"), anchor="w")
        self.move_label.pack(fill="x", pady=5)

        text_frame = tk.Frame(result_frame, bg="#e0f7fa", width=250)
        text_frame.pack(side="left", fill="y", padx=10)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        
        

        self.path_text = tk.Text(text_frame, wrap="word", yscrollcommand=scrollbar.set,
                                 bg="#ffffff", fg="#004d40", font=("Arial", 16), height=15, width=20)
        self.path_text.pack(side="left", fill="y")
        scrollbar.config(command=self.path_text.yview)

        self.time_label = tk.Label(result_frame, text="Thời gian: ", bg="#e0f7fa", fg="#004d40", font=("Arial", 14, "bold"), anchor="w")
        self.time_label.pack(fill="x", pady=5)

        self.solution_path = []
        self.current_step = 0
        self.is_animating = False

        self.setup_entry_navigation(self.initial_entries, self.goal_entries)
        self.setup_entry_navigation(self.goal_entries)

    def copy_initial_to_current(self):
        for i in range(3):
            for j in range(3):
                value = self.initial_entries[i][j].get()
                self.current_entries[i][j].config(state="normal")
                self.current_entries[i][j].delete(0, tk.END)
                self.current_entries[i][j].insert(0, value)
                self.current_entries[i][j].config(state="readonly")

    def solve_puzzle(self):
        initial_state = parse_input(self.initial_entries)
        goal_state = parse_input(self.goal_entries)

        if initial_state is None or goal_state is None:
            return

        algo = self.algo_var.get()
        self.start_time = time.time()

        print(f"Thuật toán được chọn: {self.algo_var.get()}")

        try:
            if algo == "BFS":
                path = bfs(initial_state, goal_state)
            elif algo == "DFS":
                path = dfs(initial_state, goal_state)
            elif algo == "IDS":
                path = ids(initial_state, goal_state)
            elif algo == "UCS":
                path = ucs(initial_state, goal_state)
            elif algo == "Greedy Search":
                path = greedy_search(initial_state, goal_state)
            elif algo == "A* Search":
                path = astar(initial_state, goal_state)
            elif algo == "IDA* Search":
                path = ida_star(initial_state, goal_state)
            elif algo == "Hill Climbing":
                solver = HillClimbing()
                path = solver.solve(initial_state, goal_state)
            elif algo == "Steepest-Ascent Hill Climbing":
                solver = SteepestAscentHillClimbing()
                path = solver.solve(initial_state, goal_state)
            elif algo == "Stochastic Hill Climbing":
                solver = StochasticHillClimbing()
                path = solver.solve(initial_state, goal_state)   
            elif algo == "Simulated Annealing":
                solver = SimulatedAnnealing()
                path = solver.solve(initial_state, goal_state)   
            elif algo == "Beam Search":
                solver = BeamSearch()
                path = solver.solve(initial_state, goal_state)
            elif algo == "And-Or Search":
                path = and_or_search(initial_state, goal_state)  
                if path == 'Failure':
                    messagebox.showerror("Lỗi", "Không tìm thấy lời giải! Có thể bài toán không khả thi.")
                    return
            elif algo == "Belief State Search":
                path = belief_state_search({initial_state}, goal_state, top_k=5, max_steps=200)
                if not path:
                    messagebox.showerror("Lỗi", "Không tìm thấy lời giải trong không gian trạng thái niềm tin!")
                    return
            elif algo == "Backtracking Search":
                path = Backtracking_Search(initial_state, goal_state)  
                if path == 'Failure':
                    messagebox.showerror("Lỗi", "Không tìm thấy lời giải! Có thể bài toán không khả thi.")
                    return
            elif algo == "Searching partically":
                path = searching_partically(initial_state, goal_state)  
                if path == 'Failure':
                    messagebox.showerror("Lỗi", "Không tìm thấy lời giải! Có thể bài toán không khả thi.")
                    return
            elif algo == "GA":
                path = genetic(initial_state, goal_state)  
                if path == 'Failure':
                    messagebox.showerror("Lỗi", "Không tìm thấy lời giải! Có thể bài toán không khả thi.")
                    return
            elif algo == "Q-Learning":
                path = q_learning(initial_state, goal_state)
                if path is None:
                  messagebox.showerror("Lỗi", "Không tìm thấy lời giải sau khi học Q-Learning.")
                  return
            elif algo == "Sarsa":
                path = sarsa(initial_state, goal_state)
                if path is None:
                  messagebox.showerror("Lỗi", "Không tìm thấy lời giải! Có thể bài toán không khả thi.")
                  return
            elif algo == "Backtracking with Forward Checking":
                path = backtracking_with_forward_checking(initial_state, goal_state)
                if path is None:
                  messagebox.showerror("Lỗi", "Không tìm thấy lời giải! Có thể bài toán không khả thi.")
                  return
            else:
                messagebox.showerror("Lỗi", "Vui lòng chọn thuật toán hợp lệ!")
                return
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi chạy thuật toán: {str(e)}")
            self.time_label.config(text=f"Thời gian: {0:.2f}s")
            self.move_label.config(text="Số bước: 0")
            return

        elapsed_time = time.time() - self.start_time

        if path:
            self.solution_path = path
            self.current_step = 0
            self.is_animating = True
            self.animate_path()

            self.time_label.config(text=f"Thời gian: {elapsed_time:.2f}s")
            self.move_label.config(text=f"Số bước: {len(path) - 1}")
        else:
            self.path_text.config(state="normal")
            self.path_text.delete("1.0", tk.END)
            self.path_text.insert(tk.END, "Không tìm thấy lời giải!\n")
            self.path_text.config(state="disabled")
 
            self.time_label.config(text=f"Thời gian: {elapsed_time:.2f}s")
            self.move_label.config(text="Số bước: 0")

    def format_state_as_matrix(self, state):
        """Định dạng trạng thái thành ma trận 3x3."""
        matrix = ""
        for i in range(0, 9, 3):
            row = state[i:i+3]
            matrix += " ".join(f"{num:2}" for num in row) + "\n"
        return matrix

    def animate_path(self):
        """Hiển thị từng bước của lời giải dưới dạng ma trận 3x3."""
        if self.current_step < len(self.solution_path):
            self.display_state(self.current_entries, self.solution_path[self.current_step])
            
            # Định dạng tất cả các bước dưới dạng ma trận
            formatted_path = ""
            for i, state in enumerate(self.solution_path):
                formatted_path += f"Bước {i+1}:\n"
                formatted_path += self.format_state_as_matrix(state)
                formatted_path += "\n"

            self.path_text.config(state="normal")
            self.path_text.delete("1.0", tk.END)
            self.path_text.insert(tk.END, formatted_path)
            self.path_text.config(state="disabled")

            self.move_label.config(text=f"Bước hiện tại: {self.current_step + 1}/{len(self.solution_path)}")
            self.root.after(500, self.animate_path)
            self.current_step += 1
        else:
            self.is_animating = False
            self.time_label.config(text=f"Thời gian: {(time.time() - self.start_time):.2f}s")

    def display_state(self, entries, state):
        """Hiển thị trạng thái trên lưới nhập."""
        for i in range(3):
            for j in range(3):
                entry = entries[i][j]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.insert(0, str(state[i * 3 + j]))
                entry.config(state="readonly")

    def reset_puzzle(self):
        """Đặt lại giao diện về trạng thái ban đầu."""
        for grid in [self.initial_entries, self.goal_entries]:
            for row in grid:
                for entry in row:
                    entry.delete(0, tk.END)
        self.move_label.config(text="Bước hiện tại: ")
        self.time_label.config(text="Thời gian: ")
        self.solution_path = []
        self.current_step = 0
        self.is_animating = False
        self.path_text.config(state="normal")
        self.path_text.delete("1.0", tk.END)
        self.path_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()