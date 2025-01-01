from manim import *
from lib.maze import Maze
from lib.solver import MazeSolver


class AnimateMaze(Scene):
    def construct(self):
        # 1. Introduction Scene
        title = Text("Optimal path finding.", font_size=64)
        body = Text(
            """
            Given a maze containing wall and targets
            find the point from which the total
            distance to all targets is minimized.
            """,
            font_size=32,
        )
        VGroup(title, body).arrange(DOWN, buff=1)

        self.play(Write(title))
        self.wait(1)
        self.play(Write(body))
        self.wait(3)
        self.play(FadeOut(title, body, shift=OUT))

        # 2. Maze Generation
        maze = Maze(
            rows=25, cols=60, n_targets=16, fill_fraction=0.25, random_seed=None
        )

        boxes = VGroup(
            *[
                Text(
                    s,
                    t2c={maze.wall_cell: WHITE, maze.target_cell: RED},  # type: ignore
                ).scale(0.5)
                for s in maze.get_all_cell_values()
            ]
        )
        boxes.arrange_in_grid(
            buff=(0.0, 0.0),
            rows=maze.num_rows,
            cols=maze.num_cols,
            flow_order="rd",
        )
        self.play(ShowIncreasingSubsets(boxes), run_time=5)
        self.wait(1)

        # 3. Optimal Point
        solver = MazeSolver(maze)
        optimal_point, min_dist = solver.find_optimal_point()

        def get_box_coordinates(grid_row, grid_col) -> tuple[float, float, float]:
            top_left_corner = boxes[0].get_center()
            delta_x = boxes[1].get_center()[0] - top_left_corner[0]
            delta_y = boxes[maze.num_cols].get_center()[1] - top_left_corner[1]
            new_point_x = top_left_corner[0] + (grid_col * delta_x)
            new_point_y = top_left_corner[1] + (grid_row * delta_y)
            return [new_point_x, new_point_y, 0.0]  # type: ignore

        optimal_mark = Cross(
            stroke_color=GREEN, scale_factor=0.125, stroke_width=8
        ).move_to(get_box_coordinates(*optimal_point))
        self.play(Indicate(optimal_mark), run_time=1)
        self.wait(1)

        # 4. Path Animation
        paths = solver.get_paths_from_point(optimal_point)
        path_points = VGroup(
            *[
                Text("+", font_size=32, color=BLUE, stroke_width=0, weight=BOLD)
                .move_to(get_box_coordinates(*point))
                .scale(0.5)
                for point in paths
            ]
        )
        self.add(path_points)
        self.play(Write(path_points), run_time=4)
        self.wait(4)

        # 5. Conclusion Scene
        conclusion_text = Text("Solution Achieved!", font_size=48, font="Noto Sans")
        summary = (
            VGroup(
                Text(
                    f"Optimal Point: ({optimal_point[0]}, {optimal_point[1]})",
                    font_size=36,
                ),
                Text(f"Total Distance: {min_dist}", font_size=36),
            )
            .arrange(direction=DOWN)
            .next_to(conclusion_text, DOWN)
        )
        self.play(FadeOut(*boxes, optimal_mark, path_points, optimal_mark))
        self.play(Write(conclusion_text))
        self.play(FadeIn(summary))
        self.wait(2)

        self.play(FadeOut(conclusion_text, summary))
