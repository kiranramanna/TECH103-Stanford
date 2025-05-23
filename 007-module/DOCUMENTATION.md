# Solar System Visualization Documentation

## Overview

This project implements a 3D solar system visualization using Manim Community Edition. The visualization includes the Sun and eight planets (Mercury through Neptune) with:

- Accurate relative sizing (scaled for visibility)
- Realistic orbital distances (scaled)
- Correct relative orbital speeds

## Implementation Details

### Class Structure

The implementation uses a single class `SolarSystemScene` that extends Manim's `ThreeDScene` to enable 3D rendering capabilities.

```python
class SolarSystemScene(ThreeDScene):
    def construct(self):
        # Implementation here
```

### Camera Setup

The camera is positioned to provide a good view of the entire solar system:

```python
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
self.camera.frame_center = ORIGIN
```

- `phi`: Controls the vertical viewing angle (75 degrees)
- `theta`: Controls the horizontal viewing angle (30 degrees)

### Planet Data

Each celestial body is represented by a tuple containing:
1. Name
2. Radius (scaled for visibility)
3. Orbital distance from Sun (in AU, scaled)
4. Color (using Manim's built-in colors)
5. Orbital period (in Earth days)

```python
planet_data = [
    ("Sun", 0.5, 0, YELLOW, 0),
    ("Mercury", 0.08, 1.5, LIGHT_BROWN, 88),
    # ... other planets
]
```

### Creating Celestial Bodies

The Sun is created at the origin (0, 0, 0):

```python
sun = Sphere(radius=radius, resolution=(32, 32))
sun.set_color(color)
```

Each planet is:
1. Created as a Sphere
2. Positioned along its orbit path
3. Added to the scene

```python
planet = Sphere(radius=radius, resolution=(32, 32))
planet.set_color(color)
```

### Orbital Paths

Orbits are implemented as circles rotated to lie in the x-y plane:

```python
orbit = Circle(radius=distance)
orbit.set_color(WHITE)
orbit.set_opacity(0.2)
orbit.rotate(90 * DEGREES, RIGHT)
```

### Animation

The orbital animation uses Manim's `Rotating` animation, with speeds scaled proportionally to actual orbital periods:

```python
rotation_rate = max_run_time * (365 / period) * 2 * PI
```

This formula ensures that:
- Faster planets (shorter periods) rotate more during the animation
- The relative speeds maintain the correct proportions

The animations for all planets are played simultaneously:

```python
self.play(*animations)
```

## Technical Considerations

- **Resolution**: The spheres use a resolution of (32, 32) for a balance between visual quality and performance
- **Scale**: Sizes and distances are not to actual scale (which would make inner planets nearly invisible)
- **Duration**: The animation runs for 10 seconds by default, which can be adjusted

## Limitations and Future Improvements

- Planet textures are not implemented
- Moons and other celestial bodies are not included
- Orbital planes are all perfectly aligned (no inclination)
- Planetary axial tilts are not implemented 