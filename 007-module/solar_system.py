from manim import *
import numpy as np

class SolarSystemScene(ThreeDScene):
    def construct(self):
        # Camera setup for 3D viewing
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.camera.frame_center = ORIGIN
        
        # Planet data: name, relative radius (scaled for visibility), 
        # orbital distance (in AU, scaled), color, orbital period (in Earth days)
        planet_data = [
            ("Sun", 0.5, 0, YELLOW, 0),
            ("Mercury", 0.08, 1.5, "#A86235", 88),
            ("Venus", 0.15, 2.2, GOLD, 225),
            ("Earth", 0.15, 3.0, BLUE, 365),
            ("Mars", 0.12, 3.8, RED, 687),
            ("Jupiter", 0.35, 5.0, "#E9A668", 4333),
            ("Saturn", 0.3, 6.5, "#E9D68D", 10759),
            ("Uranus", 0.25, 8.0, "#96D6CC", 30687),
            ("Neptune", 0.25, 9.5, "#3E54E8", 60190)
        ]
        
        # Create the celestial bodies
        celestial_bodies = {}
        
        for name, radius, distance, color, period in planet_data:
            if name == "Sun":
                # Create the Sun at the center
                sun = Sphere(radius=radius, resolution=(32, 32))
                sun.set_color(color)
                celestial_bodies[name] = sun
                self.add(sun)
            else:
                # Create the planet
                planet = Sphere(radius=radius, resolution=(32, 32))
                planet.set_color(color)
                
                # Create orbit path
                orbit = Circle(radius=distance)
                orbit.set_color(WHITE)
                orbit.set_opacity(0.2)
                orbit.rotate(90 * DEGREES, RIGHT)
                
                # Position the planet initially
                planet.move_to(orbit.point_at_angle(0))
                
                # Add orbit and planet to scene
                self.add(orbit, planet)
                celestial_bodies[name] = planet
        
        # Create animations for planetary orbits
        max_run_time = 10  # Animation duration in seconds
        
        # Create animations for each planet
        animations = []
        for name, radius, distance, color, period in planet_data:
            if name != "Sun" and period > 0:
                # Scale period to make animation visible
                # Faster planets should rotate more during the animation
                rotation_rate = max_run_time * (365 / period) * 2 * PI
                
                planet = celestial_bodies[name]
                
                # Create rotation animation around the Sun
                orbit_center = ORIGIN
                orbit_axis = UP
                
                animations.append(
                    Rotating(
                        planet,
                        angle=rotation_rate,
                        about_point=orbit_center,
                        axis=orbit_axis,
                        run_time=max_run_time,
                        rate_func=linear
                    )
                )
        
        # Play all animations simultaneously
        self.play(*animations)
        self.wait(2)