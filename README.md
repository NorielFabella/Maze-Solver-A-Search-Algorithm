# Maze Solver: A* Search

An engaging Python/Tkinter tool that builds random mazes, lets you pick start and finish points, then simultaneously shows an uninformed DFS trail and the guaranteed-shortest A* route. Ideal for visual learners and anyone curious about how heuristics speed up search.

🌐 **Project Snapshot**  
- **Maze Creation**: Carve out a perfect N×N maze using randomized DFS, then punch through ~5% extra walls to create alternate corridors.  
- **Dual Pathfinding**:  
  - **Depth-First Search (DFS):** a simple “follow-the-wall” strategy that eventually reaches the goal—but often meanders.  
  - **A* Search:** combines actual cost (g) with an admissible heuristic (h = Manhattan distance) to home in on the finish in the fewest steps.  
- **User Controls**: Click to place **Start** and **End**, then hit **Solve** to watch both paths draw in real time. Hit **Reset** to spin up a brand-new maze.

🔍 **Why This Matters**  
Every loopy maze hides myriad possible routes. Without guidance, blind search can waste time exploring long detours. A* ensures you get the shortest-ever path while keeping computations fast enough for an interactive demo.

⚙️ **Under the Hood**  
1. **g(n):** steps taken so far from the start cell  
2. **h(n):** Manhattan distance estimate to the goal  
3. **f(n) = g(n) + h(n):** priority score—lowest f(n) is expanded first  
4. **Reconstruction:** follow parent pointers backward once the goal is dequeued

📁 **Repository Contents**  
- `src/maze_solver_app.py` – full application code (maze gen, DFS, A*, UI)  
- `docs/research_paper.md` – detailed write-up: literature review, methods, experiments (10×10 to 50×50), results, discussion, and references  
- `slides/` – PowerPoint slides summarizing the project  
- `.gitignore`, `LICENSE`, `requirements.txt` – standard project scaffolding  

🚀 **Quickstart**  
1. **Clone**  
   ```bash
   git clone https://github.com/your-username/labyrinth-navigator.git
   cd labyrinth-navigator
   ```  
2. **Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```  
3. **Launch**  
   ```bash
   python src/maze_solver_app.py
   ```  
4. **Interact**  
   - Click **“Set Start”**, then choose a cell  
   - Click **“Set Goal”**, then choose a cell  
   - Press **“Solve”** to draw the **DFS** path (orange) and the **A*** path (blue)  
   - Press **“Reset”** to generate a fresh labyrinth  

🔗 **Further Exploration**  
- Extend to 8-direction movement with an octile distance heuristic  
- Plug in D* Lite for dynamic maze updates  
- Assign variable traversal costs (weighted regions)  

Happy navigating—and may your heuristic always guide you true! 🧭✨
