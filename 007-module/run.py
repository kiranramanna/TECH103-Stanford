#!/usr/bin/env python3
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Default to medium quality if no argument is provided
quality = "m"
if len(sys.argv) > 1 and sys.argv[1] in ["l", "m", "h"]:
    quality = sys.argv[1]

print(f"Rendering solar system visualization with quality: {quality}")

# Set resolution based on quality
if quality == "l":
    dpi = 80
    fps = 15
elif quality == "h":
    dpi = 200
    fps = 30
else:  # medium
    dpi = 120
    fps = 24

# Planet data: name, relative radius (scaled for visibility), 
# orbital distance (in AU, scaled), color, orbital period (in Earth days)
planet_data = [
    ("Sun", 0.5, 0, "yellow", 0),
    ("Mercury", 0.08, 1.5, "#A86235", 88),
    ("Venus", 0.15, 2.2, "gold", 225),
    ("Earth", 0.15, 3.0, "blue", 365),
    ("Mars", 0.12, 3.8, "red", 687),
    ("Jupiter", 0.35, 5.0, "#E9A668", 4333),
    ("Saturn", 0.3, 6.5, "#E9D68D", 10759),
    ("Uranus", 0.25, 8.0, "#96D6CC", 30687),
    ("Neptune", 0.25, 9.5, "#3E54E8", 60190)
]

# Create a figure and a 3D axis
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.set_xlabel('X (AU)')
ax.set_ylabel('Y (AU)')
ax.set_zlabel('Z (AU)')
ax.set_title('Solar System Animation')

# Set the limits based on the furthest planet
max_distance = max([distance for _, _, distance, _, _ in planet_data])
ax.set_xlim(-max_distance*1.2, max_distance*1.2)
ax.set_ylim(-max_distance*1.2, max_distance*1.2)
ax.set_zlim(-max_distance*0.6, max_distance*0.6)

# Create orbit circles
for name, radius, distance, color, period in planet_data:
    if name != "Sun":
        theta = np.linspace(0, 2*np.pi, 100)
        x = distance * np.cos(theta)
        y = distance * np.sin(theta)
        z = np.zeros_like(theta)
        ax.plot(x, y, z, color='white', alpha=0.2)

# Create the initial planets as scatter points
planets = {}
for name, radius, distance, color, period in planet_data:
    if name == "Sun":
        # Create the Sun at the center
        sun = ax.scatter([0], [0], [0], s=radius*1000, c=color, alpha=1.0, edgecolors='none')
        planets[name] = sun
    else:
        # Create the planet at initial position
        x = distance
        y = 0
        z = 0
        planet = ax.scatter([x], [y], [z], s=radius*500, c=color, alpha=1.0, edgecolors='none')
        planets[name] = planet

# Animation function
def animate(frame):
    for name, radius, distance, color, period in planet_data:
        if name != "Sun" and period > 0:
            # Calculate rotation factor based on period
            rotation_factor = (frame / 50) * (365 / period) * 2 * np.pi
            x = distance * np.cos(rotation_factor)
            y = distance * np.sin(rotation_factor)
            z = 0  # Keeping on same plane for simplicity
            planets[name]._offsets3d = ([x], [y], [z])
    return planets.values()

# Create animation
animation_length_seconds = 10
frames = animation_length_seconds * fps
ani = FuncAnimation(fig, animate, frames=frames, interval=1000/fps, blit=False)

# Save the animation
print("Saving animation...")
output_file = "solar_system_animation.gif"
ani.save(output_file, writer='pillow', fps=fps, dpi=dpi)
print(f"Animation saved as {output_file}")

# Display the animation
plt.show()