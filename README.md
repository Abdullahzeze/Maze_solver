# Maze Solver

Generate a random maze and compare three classic pathfinding algorithms: **Breadth-First Search (BFS)**, **Depth-First Search (DFS)**, and **A\***.

The Jupyter notebook visualizes the generated maze, animates each algorithm's exploration and solution path, and compares the number of explored cells and the resulting path lengths.

## Algorithms

| Algorithm | Frontier | Shortest path? | Strategy |
|---|---|---:|---|
| BFS | FIFO queue | Yes (unweighted grid) | Explores outward in expanding layers |
| DFS | LIFO stack | No guarantee | Follows one branch deeply, then backtracks |
| A* | Priority queue | Yes (with this heuristic and unit costs) | Uses path cost plus Manhattan distance to guide search |

## Project structure

```text
Maze_solver/
├── README.md
├── maze.ipynb
├── requirements.txt
├── src/
│   └── maze_solver.py
└── .gitignore
```

## Getting started

Python 3.9 or newer is recommended.

1. Clone the repository:

   ```bash
   git clone https://github.com/Abdullahzeze/Maze_solver.git
   cd Maze_solver
   ```

2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Run the notebook:

   ```bash
   jupyter notebook maze.ipynb
   ```

Run the notebook cells from top to bottom. It generates a reproducible maze using seed `7`, runs all three solvers, displays their animations, and plots a comparison.

## Use the solver module

The reusable implementation is in `src/maze_solver.py`. Add the `src` directory to your Python path, then:

```python
from maze_solver import generate_maze, solve

maze = generate_maze(15, 15, loops=25, seed=7)
start = (1, 1)
goal = (maze.shape[0] - 2, maze.shape[1] - 2)

explored, path = solve(maze, start, goal, algo="astar")
print("Explored cells:", len(explored))
print("Path length:", len(path) if path else "No path found")
```

The maze is a NumPy array where `1` represents a wall and `0` represents an open cell. Coordinates are `(row, column)`.

## Dependencies

- NumPy
- Matplotlib
- Jupyter

## Notes

- BFS and A* return a shortest path for this unweighted, four-directional grid.
- DFS returns a valid path when one exists, but it is not guaranteed to be shortest.
- The number of explored cells and path length depend on the generated maze and neighbor traversal order.
