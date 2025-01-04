from manim import *
from lib.maze3d import Maze3D
from dataclasses import dataclass
import numpy as np


@dataclass
class MazeConfig:
    layers: int = 20
    rows: int = 20
    cols: int = 40
    n_targets: int = 16
    fill_fraction: float = 0.3
    scale_factor: float = 1.0
    side_length: float = 0.5

    def __post_init__(self):
        self.layers = int(self.layers * self.scale_factor)
        self.rows = int(self.rows * self.scale_factor)
        self.cols = int(self.cols * self.scale_factor)
        self.n_targets = int(self.n_targets * self.scale_factor)


def maze_idx_to_coords(
    idx: tuple, maze: Maze3D, side_length: float
) -> tuple[float, float, float]:

    # Consider the maze to be centered at the origin, we want the maze 0th cell to be at the front facing top-left corner.
    # i.e [0, 0, 0] ~ negative X-axis, positive Y-axis, positive Z-axis
    # rows => Y-axis, cols => X-axis, layers => Z-axis

    l, r, c = idx

    row_centers = np.linspace(
        side_length * (maze.num_rows - 1) / 2,
        -side_length * (maze.num_rows - 1) / 2,
        maze.num_rows,
    )
    col_centers = np.linspace(
        -side_length * (maze.num_cols - 1) / 2,
        side_length * (maze.num_cols - 1) / 2,
        maze.num_cols,
    )
    layer_centers = np.linspace(
        side_length * (maze.num_layers - 1) / 2,
        -side_length * (maze.num_layers - 1) / 2,
        maze.num_layers,
    )

    center = (float(col_centers[c]), float(row_centers[r]), float(layer_centers[l]))
    return center


class AnimateMaze3d(ThreeDScene):

    def setup(self):

        self.maze_config = MazeConfig(scale_factor=1.0, side_length=0.25)

        self.maze = Maze3D(
            layers=self.maze_config.layers,
            rows=self.maze_config.rows,
            cols=self.maze_config.cols,
            n_targets=self.maze_config.n_targets,
            fill_fraction=self.maze_config.fill_fraction,
            random_seed=None,
        )
        self.color_fill = {
            self.maze.wall_cell: WHITE,
            self.maze.target_cell: RED,
            self.maze.empty_cell: BLACK,
        }
        self.opacity_fill = {
            self.maze.wall_cell: 0.25,
            self.maze.target_cell: 0.75,
            self.maze.empty_cell: 0.0,
        }

    def _get_maze_cell(self, idx: tuple, cell_type: str) -> Cube:
        return Cube(
            side_length=(
                (2 / 3) * self.maze_config.side_length
                if cell_type != self.maze.wall_cell
                else (1 / 3) * self.maze_config.side_length
            ),
            fill_color=self.color_fill[cell_type],
            fill_opacity=self.opacity_fill[cell_type],
            stroke_opacity=self.opacity_fill[cell_type],
            background_stroke_opacity=self.opacity_fill[cell_type],
        ).move_to(
            maze_idx_to_coords(
                idx,
                self.maze,
                self.maze_config.side_length,
            )
        )

    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # 1. Setup the maze on the screen
        walls = VGroup(
            *[
                self._get_maze_cell(idx, self.maze.wall_cell)
                for idx in self.maze.get_wall_cells()
            ]
        )

        targets = VGroup(
            *[
                self._get_maze_cell(idx, self.maze.target_cell)
                for idx in self.maze.get_target_cells()
            ]
        )

        full_graph = VGroup(walls, targets)

        self.play(ShowIncreasingSubsets(full_graph), run_time=2)

        # 2. Rotate the camera to view the maze from different angles.
        self.begin_3dillusion_camera_rotation(rate=0.5)
        self.wait(3)
        self.stop_3dillusion_camera_rotation()
