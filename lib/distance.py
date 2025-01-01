from collections import deque
from lib.maze import Maze


def reconstruct_path(parent_map, start, goal):
    """
    Reconstructs a path from start -> goal using parent_map.
    Returns a list of cells (row, col) in order, or an empty list if unreachable.
    """
    if goal not in parent_map:
        return []

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent_map[current]  # step to parent
    path.reverse()  # because we built it backwards
    return path if path and path[0] == start else []


class DistanceCalculator:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.num_rows = maze.num_rows
        self.num_cols = maze.num_cols
        self.directions = [
            (x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if (x, y) != (0, 0)
        ]

    def bfs_distance_with_parents(
        self, start_row: int, start_col: int
    ) -> tuple[dict, dict]:
        """
        Performs BFS from (start_r, start_c).
        Returns:
            distance_map, parent_map
        where:
            distance_map[(r,c)] = BFS distance from start -> (r,c)
            parent_map[(r,c)] = (prev_r, prev_c) in the BFS tree
                                or None if (r,c) is the start node.
        """
        visited = set()
        distance_map = {}
        parent_map = {}

        queue = deque([(start_row, start_col)])
        distance_map[(start_row, start_col)] = 0
        visited.add((start_row, start_col))
        parent_map[(start_row, start_col)] = None  # no parent for the start

        while queue:
            r, c = queue.popleft()
            current_dist = distance_map[(r, c)]

            for dr, dc in self.directions:
                nr, nc = r + dr, c + dc
                if self._is_valid_cell(nr, nc) and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    distance_map[(nr, nc)] = current_dist + 1
                    queue.append((nr, nc))
                    parent_map[(nr, nc)] = (r, c)

        return distance_map, parent_map

    def _is_valid_cell(self, r, c):
        """
        Returns True if in-bounds and not a wall ('#').
        """
        if 0 <= r < self.num_rows and 0 <= c < self.num_cols:
            return self.maze[r][c] != self.maze.wall_cell
        return False
