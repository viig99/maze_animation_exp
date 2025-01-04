import numpy as np
import random
import matplotlib.pyplot as plt


class Maze3D:
    def __init__(
        self,
        layers=20,
        rows=20,
        cols=40,
        n_targets=16,
        fill_fraction=0.3,
        wall_cell="#",
        empty_cell=" ",
        target_cell="*",
        random_seed=None,
    ):
        self.num_layers = layers
        self.num_rows = rows
        self.num_cols = cols
        self.n_targets = n_targets
        self.fill_fraction = fill_fraction
        self.wall_cell = wall_cell
        self.empty_cell = empty_cell
        self.target_cell = target_cell

        if random_seed is not None:
            random.seed(random_seed)
            np.random.seed(random_seed)

        self.grid = np.full(
            (self.num_layers, self.num_rows, self.num_cols), self.empty_cell, dtype=str
        )

        self._random_fill_interior()
        self._place_targets(self.n_targets)

    def __str__(self) -> str:
        return "\n\n".join(
            [
                f"Layer {l}:\n" + "\n".join("".join(row) for row in self.grid[l])
                for l in range(self.num_layers)
            ]
        )

    def _random_fill_interior(self):
        random_mask = np.random.random((self.num_layers, self.num_rows, self.num_cols))
        interior = np.where(
            random_mask > self.fill_fraction, self.empty_cell, self.wall_cell
        )
        self.grid = interior

    def _place_targets(self, n_targets):
        empty_cells = self.get_empty_cells()
        if len(empty_cells) < n_targets:
            raise ValueError(
                f"Warning: Only {len(empty_cells)} empty cells available for {n_targets} targets."
            )

        selected_cells = random.sample(empty_cells, n_targets)
        for l, r, c in selected_cells:
            self.grid[l, r, c] = self.target_cell

    def get_empty_cells(self):
        return list(zip(*np.where(self.grid == self.empty_cell)))

    def get_target_cells(self):
        return list(zip(*np.where(self.grid == self.target_cell)))

    def get_wall_cells(self):
        return list(zip(*np.where(self.grid == self.wall_cell)))

    def plot_3d_maze(self):
        """
        Plots the 3D maze using matplotlib.
        """
        wall_cells = self.get_wall_cells()
        empty_cells = self.get_empty_cells()
        target_cells = self.get_target_cells()

        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection="3d")

        # Plot wall cells
        if wall_cells:
            wall_x, wall_y, wall_z = zip(*wall_cells)
            ax.scatter(wall_x, wall_y, wall_z, c="black", marker="X", label="Walls")

        # Plot empty cells
        if empty_cells:
            empty_x, empty_y, empty_z = zip(*empty_cells)
            ax.scatter(
                empty_x, empty_y, empty_z, c="white", label="Paths"  # edgecolor="black"
            )

        # Plot target cells
        if target_cells:
            target_x, target_y, target_z = zip(*target_cells)
            ax.scatter(
                target_x, target_y, target_z, c="red", marker="o", label="Targets"
            )

        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.set_zlabel("Z-axis")  # type: ignore
        ax.set_title("3D Maze Visualization")
        ax.legend()
        plt.show()


if __name__ == "__main__":
    maze3d = Maze3D(
        layers=20, rows=20, cols=40, n_targets=16, fill_fraction=0.3, random_seed=None
    )
    # print(maze3d)

    num_elements = maze3d.num_layers * maze3d.num_rows * maze3d.num_cols

    print(f"Empty cells fraction: {len(maze3d.get_empty_cells()) / num_elements:.2%}")
    print(f"Wall cells fraction: {len(maze3d.get_wall_cells()) / num_elements:.2%}")

    # Plot the 3D maze
    # maze3d.plot_3d_maze()
