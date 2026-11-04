"""Maze generation and pathfinding with BFS, DFS, and A*."""

from __future__ import annotations

import heapq
import random
from collections import deque

import numpy as np

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def generate_maze(h: int, w: int, loops: int = 0, seed: int | None = None) -> np.ndarray:
    """Generate a (2*h+1, 2*w+1) maze; 1 is wall and 0 is open."""
    if h < 1 or w < 1:
        raise ValueError("h and w must be positive")
    if loops < 0:
        raise ValueError("loops must be non-negative")

    rng = random.Random(seed)
    maze = np.ones((2 * h + 1, 2 * w + 1), dtype=int)
    maze[1, 1] = 0
    visited = {(0, 0)}
    stack = [(0, 0)]

    while stack:
        r, c = stack[-1]
        options = [
            (r + dr, c + dc)
            for dr, dc in DIRS
            if 0 <= r + dr < h and 0 <= c + dc < w
            and (r + dr, c + dc) not in visited
        ]
        if options:
            nr, nc = rng.choice(options)
            maze[r + nr + 1, c + nc + 1] = 0
            maze[2 * nr + 1, 2 * nc + 1] = 0
            visited.add((nr, nc))
            stack.append((nr, nc))
        else:
            stack.pop()

    candidates = [
        (r, c)
        for r in range(1, maze.shape[0] - 1)
        for c in range(1, maze.shape[1] - 1)
        if maze[r, c] == 1
        and (
            (maze[r - 1, c] == 0 and maze[r + 1, c] == 0)
            or (maze[r, c - 1] == 0 and maze[r, c + 1] == 0)
        )
    ]
    for r, c in rng.sample(candidates, min(loops, len(candidates))):
        maze[r, c] = 0
    return maze


def solve(maze: np.ndarray, start: tuple[int, int], goal: tuple[int, int],
          algo: str = "bfs") -> tuple[list[tuple[int, int]], list[tuple[int, int]] | None]:
    """Return (exploration_order, path); path is None if goal is unreachable."""
    if algo not in {"bfs", "dfs", "astar"}:
        raise ValueError(f"unknown algorithm: {algo}")

    height, width = maze.shape
    for point, label in ((start, "start"), (goal, "goal")):
        if not (0 <= point[0] < height and 0 <= point[1] < width):
            raise ValueError(f"{label} is outside the maze")
        if maze[point] == 1:
            raise ValueError(f"{label} must be an open cell")

    def heuristic(point: tuple[int, int]) -> int:
        return abs(point[0] - goal[0]) + abs(point[1] - goal[1])

    came_from = {start: None}
    cost = {start: 0}
    queue = deque([start])
    heap = [(heuristic(start), start)]
    explored: list[tuple[int, int]] = []
    seen = set()

    while heap if algo == "astar" else queue:
        if algo == "astar":
            _, current = heapq.heappop(heap)
        elif algo == "bfs":
            current = queue.popleft()
        else:
            current = queue.pop()

        if current in seen:
            continue
        seen.add(current)
        explored.append(current)
        if current == goal:
            break

        for dr, dc in DIRS:
            nxt = (current[0] + dr, current[1] + dc)
            if not (0 <= nxt[0] < height and 0 <= nxt[1] < width):
                continue
            if maze[nxt] == 1:
                continue

            new_cost = cost[current] + 1
            if algo == "astar":
                if nxt not in cost or new_cost < cost[nxt]:
                    cost[nxt] = new_cost
                    came_from[nxt] = current
                    heapq.heappush(heap, (new_cost + heuristic(nxt), nxt))
            elif nxt not in came_from:
                cost[nxt] = new_cost
                came_from[nxt] = current
                queue.append(nxt)

    if goal not in came_from:
        return explored, None

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    return explored, path[::-1]


def animate_solve(maze: np.ndarray, explored: list[tuple[int, int]],
                  path: list[tuple[int, int]] | None, title: str,
                  per_frame: int = 4, interval: int = 40):
    """Create a Matplotlib animation of explored cells and the final path."""
    if path is None:
        raise ValueError("Cannot animate a path that was not found")

    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from matplotlib.colors import ListedColormap

    cmap = ListedColormap(["white", "#1f2937", "#93c5fd", "#ef4444"])
    n_explore = -(-len(explored) // per_frame)
    total = n_explore + len(path)

    def canvas_at(frame):
        canvas = maze.copy()
        k = min(frame + 1, n_explore) * per_frame
        for r, c in explored[:k]:
            canvas[r, c] = 2
        if frame >= n_explore:
            for r, c in path[: frame - n_explore + 1]:
                canvas[r, c] = 3
        return canvas

    fig, ax = plt.subplots(figsize=(6, 6))
    image = ax.imshow(canvas_at(0), cmap=cmap, vmin=0, vmax=3,
                      interpolation="nearest")
    ax.axis("off")

    def update(frame):
        image.set_data(canvas_at(frame))
        if frame < n_explore:
            count = min((frame + 1) * per_frame, len(explored))
            ax.set_title(f"{title}: exploring ({count}/{len(explored)} cells)")
        else:
            ax.set_title(f"{title}: path found ({len(path)} cells)")
        return [image]

    animation = FuncAnimation(fig, update, frames=total,
                              interval=interval, blit=False)
    plt.close(fig)
    return animation


if __name__ == "__main__":
    maze = generate_maze(15, 15, loops=25, seed=7)
    start, goal = (1, 1), (maze.shape[0] - 2, maze.shape[1] - 2)
    for algorithm in ("bfs", "dfs", "astar"):
        explored, path = solve(maze, start, goal, algo=algorithm)
        print(f"{algorithm.upper():5} explored={len(explored):4} "
              f"path_cells={len(path) if path else 'unreachable'}")
