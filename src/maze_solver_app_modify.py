import tkinter as tk
from tkinter import ttk, messagebox
import random
import heapq
import time

CELL_SIZE = 20

class MazeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("A* Maze Solver")
        self.geometry("+100+50")

        self.grid_size_options = {"10x10": 10, "20x20": 20, "30x30": 30}
        self.density_options = {"10%": 0.10, "20%": 0.20, "30%": 0.30}

        self.grid_size = 30
        self.wall_density = 0.05

        self.start = (0, 0)
        self.goal = (self.grid_size - 1, self.grid_size - 1)
        self.set_mode = None

        self._setup_ui()
        self._generate_and_setup_maze()
        self._draw_grid()

    def _setup_ui(self):
        self.canvas = tk.Canvas(self, width=CELL_SIZE*self.grid_size, height=CELL_SIZE*self.grid_size)
        self.canvas.pack()

        control_frame = tk.Frame(self)
        control_frame.pack(fill=tk.X)

        tk.Button(control_frame, text="Solve", command=self.solve).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Reset Maze", command=self.reset).pack(side=tk.LEFT)

        self.size_var = tk.StringVar(value="30x30")
        self.density_var = tk.StringVar(value="10%")

        tk.Label(control_frame, text="Size:").pack(side=tk.LEFT)
        size_menu = ttk.OptionMenu(control_frame, self.size_var, "30x30", *self.grid_size_options.keys(), command=self._on_dropdown_change)
        size_menu.pack(side=tk.LEFT)

        tk.Label(control_frame, text="Density:").pack(side=tk.LEFT)
        density_menu = ttk.OptionMenu(control_frame, self.density_var, "10%", *self.density_options.keys(), command=self._on_dropdown_change)
        density_menu.pack(side=tk.LEFT)

        tk.Radiobutton(control_frame, text="Set Start", variable=tk.StringVar(value=""), value="start",
                       command=lambda: self._set_mode('start')).pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="Set Goal", variable=tk.StringVar(value=""), value="goal",
                       command=lambda: self._set_mode('goal')).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Done", command=lambda: self._set_mode(None)).pack(side=tk.LEFT)

        self.results_label = tk.Label(self, text="Avg. Path Length: 0 | Avg. Time (ms): 0")
        self.results_label.pack()

        self.canvas.bind('<Button-1>', self._on_canvas_click)

    def _on_dropdown_change(self, _=None):
        self.grid_size = self.grid_size_options[self.size_var.get()]
        self.wall_density = self.density_options[self.density_var.get()]
        self.start = (0, 0)
        self.goal = (self.grid_size - 1, self.grid_size - 1)

        self.canvas.config(width=CELL_SIZE*self.grid_size, height=CELL_SIZE*self.grid_size)
        self._generate_and_setup_maze()
        self._draw_grid()
        self._reset_results()

    def _reset_results(self):
        self.results_label.config(text="Avg. Path Length: 0 | Avg. Time (ms): 0")

    def _set_mode(self, mode):
        self.set_mode = mode
        if mode:
            self.title(f"A* Maze Solver - Click to set {mode}")
        else:
            self.title("A* Maze Solver")

    def _on_canvas_click(self, event):
        if not self.set_mode:
            return
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size and self.grid[row][col] == 0:
            if self.set_mode == 'start':
                self.start = (row, col)
            elif self.set_mode == 'goal':
                self.goal = (row, col)
            self._draw_grid()

    def _generate_and_setup_maze(self):
        self.grid = [[1 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        stack = [(0, 0)]
        visited = set(stack)
        self.grid[0][0] = 0
        while stack:
            x, y = stack[-1]
            neighbors = []
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx, ny = x + dx*2, y + dy*2
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and (nx, ny) not in visited:
                    neighbors.append((nx, ny, dx, dy))
            if neighbors:
                nx, ny, dx, dy = random.choice(neighbors)
                visited.add((nx, ny))
                self.grid[nx][ny] = 0
                self.grid[x+dx][y+dy] = 0
                stack.append((nx, ny))
            else:
                stack.pop()

        self._add_loops(int(self.grid_size * self.grid_size * self.wall_density))

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (i, j) == self.start or (i, j) == self.goal:
                    continue
                    
                if (i == 0 or i == self.grid_size-1 or j == 0 or j == self.grid_size-1):
                    if self.grid[i][j] == 1 and random.random() > self.wall_density:
                        self.grid[i][j] = 0
                    elif self.grid[i][j] == 0 and random.random() < self.wall_density * 0.3:
                        self.grid[i][j] = 1

        sx, sy = self.start
        gx, gy = self.goal
        self.grid[sx][sy] = 0
        self.grid[gx][gy] = 0

        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = gx + dx, gy + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                self.grid[nx][ny] = 0
                break

    def _add_loops(self, count):
        attempts = 0
        added = 0
        while added < count and attempts < count * 10:
            attempts += 1
            i = random.randrange(1, self.grid_size - 1)
            j = random.randrange(1, self.grid_size - 1)
            if self.grid[i][j] == 1:
                open_neighbors = []
                for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    ni, nj = i + dx, j + dy
                    if self.grid[ni][nj] == 0:
                        open_neighbors.append((dx, dy))
                if len(open_neighbors) >= 2:
                    self.grid[i][j] = 0
                    added += 1

    def _draw_grid(self, path=None, alt_path=None):
        self.canvas.delete("all")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1, y1 = j * CELL_SIZE, i * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = "white" if self.grid[i][j] == 0 else "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
        if alt_path:
            for (r, c) in alt_path:
                x1 = c * CELL_SIZE + CELL_SIZE // 4
                y1 = r * CELL_SIZE + CELL_SIZE // 4
                x2 = x1 + CELL_SIZE // 2
                y2 = y1 + CELL_SIZE // 2
                self.canvas.create_oval(x1, y1, x2, y2, fill="yellow", outline="yellow")
        sx, sy = self.start[1] * CELL_SIZE, self.start[0] * CELL_SIZE
        gx, gy = self.goal[1] * CELL_SIZE, self.goal[0] * CELL_SIZE
        self.canvas.create_rectangle(sx, sy, sx + CELL_SIZE, sy + CELL_SIZE, fill="green", outline="gray")
        self.canvas.create_rectangle(gx, gy, gx + CELL_SIZE, gy + CELL_SIZE, fill="red", outline="gray")
        if path:
            for (r, c) in path:
                x1 = c * CELL_SIZE + CELL_SIZE // 4
                y1 = r * CELL_SIZE + CELL_SIZE // 4
                x2 = x1 + CELL_SIZE // 2
                y2 = y1 + CELL_SIZE // 2
                self.canvas.create_oval(x1, y1, x2, y2, fill="blue", outline="blue")

    def solve(self):
        start_time = time.perf_counter()
        alt_path = dfs_path(self.grid, self.start, self.goal)
        path, nodes_expanded = a_star(self.grid, self.start, self.goal)
        end_time = time.perf_counter()

        if path:
            self._draw_grid(path, alt_path)
            path_length = len(path)
            time_ms = (end_time - start_time) * 1000
            self.results_label.config(
                text=f"Avg. Path Length: {path_length} | Avg. Time (ms): {time_ms:.2f}"
            )
        else:
            messagebox.showinfo("No Path", "No path could be found!")

    def reset(self):
        self.start = (0, 0)
        self.goal = (self.grid_size - 1, self.grid_size - 1)
        self._generate_and_setup_maze()
        self._draw_grid()
        self._reset_results()

def a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start))
    came_from = {}
    g_score = {start: 0}
    closed = set()
    nodes_expanded = 0

    while open_set:
        f, g, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct_path(came_from, current), nodes_expanded
        if current in closed:
            continue
        closed.add(current)
        nodes_expanded += 1
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            x, y = neighbor
            if 0 <= x < rows and 0 <= y < cols and grid[x][y] == 0 and neighbor not in closed:
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))
    return None, nodes_expanded

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def dfs_path(grid, start, goal):
    stack = [start]
    visited = set([start])
    parent = {}
    while stack:
        node = stack.pop()
        if node == goal:
            break
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            ni, nj = node[0]+dx, node[1]+dy
            if 0<=ni<len(grid) and 0<=nj<len(grid[0]) and grid[ni][nj]==0 and (ni,nj) not in visited:
                visited.add((ni,nj))
                parent[(ni,nj)] = node
                stack.append((ni,nj))
    path = []
    node = goal
    while node in parent:
        path.append(node)
        node = parent[node]
    if node == start:
        path.append(start)
        path.reverse()
        return path
    return None

if __name__ == '__main__':
    app = MazeApp()
    app.mainloop()
