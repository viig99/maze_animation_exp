# Animation Experiment

Generate a maze with wall and target's and find the point from which the distance to all targets is minimized.
Animation done using [manim](https://www.manim.community/)

## Generate Scene
```bash
manim -pqh scene.py AnimateMaze
```

## Maze Solver
```bash
python -m lib.solver
```

## Animation
![maze](assets/AnimateMaze.gif)

### Extras

```bash
convert_mp4_to_gif() {
    # Check if correct number of arguments is provided
    if [ "$#" -lt 2 ]; then
        echo "Usage: convert_mp4_to_gif <input_file> <output_file> [fps] [scale_width]"
        return 1
    fi

    # Assign arguments to variables
    local input_file="$1"
    local output_file="$2"
    local fps="${3:-15}"          # Default to 15 FPS if not provided
    local scale_width="${4:-1080}" # Default to 1080 width if not provided

    # Run the FFmpeg command
    ffmpeg -i "$input_file" -vf "fps=${fps},scale=${scale_width}:-1:flags=lanczos" -c:v gif "$output_file"

    # Check if the command succeeded
    if [ $? -eq 0 ]; then
        echo "GIF created successfully at: $output_file"
    else
        echo "An error occurred while creating the GIF."
    fi
}

convert_mp4_to_gif "media/videos/scene/1080p60/AnimateMaze.mp4" "assets/AnimateMaze.gif" 24 1080
```