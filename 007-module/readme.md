# 3D Solar System Visualization with Manim

This project creates a 3D visualization of our solar system using Manim Community Edition, featuring the Sun at the center with planets orbiting at realistic relative distances and speeds.

## Prerequisites

- Python 3.7+
- FFmpeg
- Cairo

### Installing Dependencies on macOS

```bash
# Install FFmpeg and Cairo using Homebrew
brew install ffmpeg cairo

# For LaTeX (optional, not used in this visualization)
# brew install mactex
```

### Installing Dependencies on Ubuntu/Debian

```bash
# Install FFmpeg and Cairo
sudo apt update
sudo apt install -y ffmpeg libcairo2-dev pkg-config python3-dev

# For LaTeX (optional, not used in this visualization)
# sudo apt install -y texlive-latex-base texlive-fonts-recommended
```

## Setup Instructions

### Option 1: Using venv (Standard Python)

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Using Conda

1. Create and activate a conda environment:
   ```bash
   conda create -n manim python=3.10
   conda activate manim
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Visualization

### Using the run.py script (recommended)

We've provided a simple script to run the visualization:

```bash
# For low quality (fastest)
python run.py l

# For medium quality (default)
python run.py
# or
python run.py m

# For high quality (slower)
python run.py h
```

### Using Manim module directly

Alternatively, you can use Manim commands directly:

```bash
# Low quality
python -m manim --quality=l -p solar_system.py SolarSystemScene

# Medium quality
python -m manim --quality=m -p solar_system.py SolarSystemScene

# High quality
python -m manim --quality=h -p solar_system.py SolarSystemScene
```

The `-p` flag tells Manim to play the animation after rendering is complete.

## Implementation Details

- The solar system is implemented as a 3D scene with the Sun at the center
- Planet sizes are scaled for visibility while maintaining relative proportions
- Orbital distances use Astronomical Units (AU) as a base, scaled for visualization
- Orbital speeds are calculated based on actual planetary periods (in Earth days)
- Camera is positioned to provide a view of the entire system

## Customization

You can modify the `planet_data` list in the `SolarSystemScene` class to:
- Change planet sizes, colors, or distances
- Adjust orbital periods
- Add new celestial bodies

You can also modify `max_run_time` to change the animation duration.

## Project Requirements

1. Create a 3D visualization of the solar system using Manim Community Edition
2. Implement accurate relative scaling for planet sizes and orbital distances
3. Animate orbital motion with correct relative speeds
4. Configure camera positioning for optimal viewing

## Implementation Steps

1. **Set up the project structure**
   - Create a new Python file named `solar_system.py`
   - Create a requirements.txt file with the necessary dependencies

2. **Install dependencies**
   - The project requires Python 3.7+ and Manim Community Edition

3. **Create the solar system visualization class**
   - Implement a class that extends ThreeDScene
   - Set up the camera orientation for 3D viewing
   - Create and position the Sun at the origin

4. **Add planets with accurate properties**
   - Define planet data including:
     - Name
     - Relative radius (scaled for visibility)
     - Orbital distance from Sun
     - Color
     - Orbital period in Earth days

5. **Implement orbital animations**
   - Create rotation animations for each planet
   - Adjust rotation speeds based on actual orbital periods
   - Set appropriate run time for the animation

6. **Add documentation and usage instructions**
   - Include comments explaining key implementation details
   - Provide instructions for rendering the scene

## Example Implementation Structure

```python
from manim import *

class SolarSystemScene(ThreeDScene):
    def construct(self):
        # Camera setup
        # ...

        # Create the Sun
        # ...

        # Define and create planets
        # ...

        # Implement orbital animations
        # ...
```

## Extension Ideas

- Add planet textures
- Include moons for some planets
- Add labels for each celestial body
- Implement camera movement to view the system from different angles 