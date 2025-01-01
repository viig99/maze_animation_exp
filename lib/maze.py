import random


class MazeRow:
    def __init__(self, num_cols: int, wall_cell: str, empty_cell: str):
        self.row = [wall_cell for _ in range(num_cols)]
        self.wall_cell = wall_cell
        self.empty_cell = empty_cell

    def __setitem__(self, col: int, value: str):
        self.row[col] = value

    def __getitem__(self, col: int) -> str:
        return self.row[col]

    def __str__(self) -> str:
        return "".join(self.row)

    def get_empty_cells(self) -> list[int]:
        return [i for i, cell in enumerate(self.row) if cell == self.empty_cell]


class Maze:
    def __init__(
        self,
        rows=11,
        cols=20,
        n_targets=4,
        fill_fraction=0.3,
        wall_cell="#",
        empty_cell=" ",
        target_cell="*",
        random_seed=None,
    ):
        """
        :param rows:    Total number of rows in the maze (including boundary).
        :param cols:    Total number of columns (including boundary).
        :param n_targets: How many '*' cells to place in the maze.
        :param fill_fraction: Fraction of interior cells to remain walls (0 <= fill_fraction <= 1).
                             e.g. 0.3 means ~30% of interior cells will be walls.
        :param random_seed:  If given, sets the random seed for reproducibility.
        """
        self.num_rows = rows
        self.num_cols = cols
        self.n_targets = n_targets
        self.fill_fraction = fill_fraction
        self.wall_cell = wall_cell
        self.empty_cell = empty_cell
        self.target_cell = target_cell

        if random_seed is not None:
            random.seed(random_seed)

        self.grid = [
            MazeRow(self.num_cols, self.wall_cell, self.empty_cell)
            for _ in range(self.num_rows)
        ]
        self._random_fill_interior()
        self._place_targets(self.n_targets)

    def __repr__(self) -> str:
        return f"MazeGenerator(rows={self.num_rows}, cols={self.num_cols}, n_targets={self.n_targets}, fill_fraction={self.fill_fraction})"

    def __str__(self) -> str:
        return "\n".join([str(row) for row in self.grid])

    def __getitem__(self, row: int) -> MazeRow:
        return self.grid[row]

    def _random_fill_interior(self) -> None:
        """
        Randomly assign each interior cell (not on the boundary) to be a wall_cell.
        or a empty_cell based on the fill_fraction.
        """
        for r in range(1, self.num_rows - 1):
            for c in range(1, self.num_cols - 1):
                if random.random() > self.fill_fraction:
                    self.grid[r][c] = self.empty_cell
                else:
                    self.grid[r][c] = self.wall_cell

    def _get_cell_type(self, cell_type: str) -> list[tuple[int, int]]:
        return [
            (r, c)
            for r in range(self.num_rows)
            for c in range(self.num_cols)
            if self.grid[r][c] == cell_type
        ]

    def _place_targets(self, n_targets) -> None:
        """
        Randomly choose n_targets empty cells and mark them as '*'.
        If there aren't enough empty cells, some targets won't be placed.
        """
        # Find all empty cells
        empty_cells = self.get_empty_cells()

        num_cells_to_fill = min(n_targets, len(empty_cells))

        if num_cells_to_fill < n_targets:
            raise ValueError(
                f"Warning: Only {num_cells_to_fill} empty cells available."
            )

        cell_to_fill = random.sample(empty_cells, num_cells_to_fill)
        for cell in cell_to_fill:
            (r, c) = cell
            self.grid[r][c] = self.target_cell

    def get_empty_cells(self) -> list[tuple[int, int]]:
        return self._get_cell_type(self.empty_cell)

    def get_target_cells(self) -> list[tuple[int, int]]:
        return self._get_cell_type(self.target_cell)

    def get_wall_cells(self) -> list[tuple[int, int]]:
        return self._get_cell_type(self.wall_cell)

    def get_wall_corner_cells(self) -> list[tuple[int, int]]:
        """
        Returns the corner cells of the walls.
        """
        wall_cells = self.get_wall_cells()
        wall_corners = [
            (r, c)
            for r, c in wall_cells
            if r == 0 or r == self.num_rows - 1 or c == 0 or c == self.num_cols - 1
        ]
        return wall_corners

    def get_all_cell_values(self) -> list[str]:
        return [cell for row in self.grid for cell in row.row]
