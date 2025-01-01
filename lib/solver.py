from lib.maze import Maze
from lib.distance import DistanceCalculator, reconstruct_path
from rich.console import Console


class MazeSolver:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.distance_calculator = DistanceCalculator(maze)
        self.targets = maze.get_target_cells()
        self.empty_cells = maze.get_empty_cells()

    def find_optimal_point(self) -> tuple[tuple[int, int], float]:
        """
        Returns (best_row, best_col, min_sum_of_distances).
        """
        best_cell = (-1, -1)
        best_dist_sum = float("inf")

        all_dist_maps = []
        for tr, tc in self.targets:
            dist_map, _ = self.distance_calculator.bfs_distance_with_parents(tr, tc)
            all_dist_maps.append(dist_map)

        # Now iterate over *all* possible empty cells:
        for r, c in self.empty_cells:
            # Sum distances from each target's dist_map
            dist_sum = 0
            for dist_map in all_dist_maps:
                d = dist_map.get((r, c), float("inf"))
                dist_sum += d
            if dist_sum < best_dist_sum:
                best_dist_sum = dist_sum
                best_cell = (r, c)
        return best_cell, best_dist_sum

    def mark_point(self, given_point: tuple[int, int], marking_cell_type="X") -> None:
        """
        Mark the given point with the given cell type.
        """
        r, c = given_point
        self.maze[r][c] = marking_cell_type

    def get_paths_from_point(
        self, given_point: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """
        Return the shortest paths from the given point to targets.
        """
        (start_r, start_c) = given_point
        _, parent_map = self.distance_calculator.bfs_distance_with_parents(
            start_r, start_c
        )

        paths = []
        for tr, tc in self.targets:
            path = reconstruct_path(parent_map, given_point, (tr, tc))
            for r, c in path:
                if self.maze[r][c] == self.maze.empty_cell and (r, c) != given_point:
                    paths.append((r, c))
        return paths

    def mark_paths_from_point(
        self, given_point: tuple[int, int], marking_cell_type="."
    ) -> None:
        """
        Mark the shortest paths from the given point to targets.
        """

        paths = self.get_paths_from_point(given_point)
        for path in paths:
            self.mark_point(path, marking_cell_type)


if __name__ == "__main__":
    maze = Maze(rows=25, cols=60, n_targets=16, fill_fraction=0.25, random_seed=None)

    solver = MazeSolver(maze)
    best_cell, best_dist_sum = solver.find_optimal_point()
    print("Best cell:", best_cell, "with sum of distances =", best_dist_sum)

    solver.mark_point(given_point=best_cell, marking_cell_type="X")
    solver.mark_paths_from_point(best_cell, marking_cell_type=".")
    console = Console()

    maze_str = str(maze)

    # assign different colors to different cell types
    maze_str = maze_str.replace(maze.wall_cell, f"[white]{maze.wall_cell}[/]")
    maze_str = maze_str.replace("X", f"[bold green]X[/]")
    maze_str = maze_str.replace(maze.target_cell, f"[bold violet]{maze.target_cell}[/]")
    maze_str = maze_str.replace(".", f"[bold blue].[/]")

    console.print(maze_str)
