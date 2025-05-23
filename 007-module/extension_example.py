from manim import *
import numpy as np
from solar_system import SolarSystemScene

class ExtendedSolarSystemScene(SolarSystemScene):
    def construct(self):
        # First set up the basic solar system
        # Camera setup for 3D viewing
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.camera.frame_center = ORIGIN
        
        # Planet data with same format as original, but adding a few moons
        # Format: name, radius, distance, color, period
        planet_data = [
            ("Sun", 0.5, 0, YELLOW, 0),
            ("Mercury", 0.08, 1.5, LIGHT_BROWN, 88),
            ("Venus", 0.15, 2.2, GOLD, 225),
            ("Earth", 0.15, 3.0, BLUE, 365),
            ("Mars", 0.12, 3.8, RED, 687),
            ("Jupiter", 0.35, 5.0, ORANGE, 4333),
            ("Saturn", 0.3, 6.5, LIGHT_BROWN, 10759),
            ("Uranus", 0.25, 8.0, TEAL, 30687),
            ("Neptune", 0.25, 9.5, BLUE_E, 60190)
        ]
        
        # Moons data: parent planet, name, radius, distance from planet, color, period
        moon_data = [
            ("Earth", "Moon", 0.04, 0.4, LIGHT_GREY, 27),
            ("Jupiter", "Io", 0.03, 0.5, YELLOW_E, 1.8),
            ("Jupiter", "Europa", 0.03, 0.65, WHITE, 3.6),
            ("Saturn", "Titan", 0.05, 0.6, GOLD_E, 16)
        ]
        
        # Create celestial bodies
        celestial_bodies = {}
        
        # Add sun and planets (similar to original)
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
        
        # Add moons
        moon_objects = {}
        for parent, name, radius, distance, color, period in moon_data:
            # Create the moon
            moon = Sphere(radius=radius, resolution=(24, 24))
            moon.set_color(color)
            
            # The planet position will be the center of the moon's orbit
            parent_planet = celestial_bodies[parent]
            
            # Create a small orbit for the moon around its planet
            moon_orbit = Circle(radius=distance)
            moon_orbit.set_color(WHITE)
            moon_orbit.set_opacity(0.1)
            moon_orbit.rotate(90 * DEGREES, RIGHT)
            
            # Move the orbit to be centered on the planet's current position
            moon_orbit.move_to(parent_planet.get_center())
            
            # Position the moon initially
            moon.move_to(moon_orbit.point_at_angle(0))
            
            # Add moon and its orbit to the scene
            self.add(moon_orbit, moon)
            moon_objects[(parent, name)] = (moon, parent_planet)
        
        # Create animations for planetary orbits
        max_run_time = 10  # Animation duration in seconds
        
        # Create animations for planets
        animations = []
        for name, radius, distance, color, period in planet_data:
            if name != "Sun" and period > 0:
                # Scale period to make animation visible
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
        
        # Create animations for moons
        moon_animations = []
        for (parent, name), (moon, parent_planet) in moon_objects.items():
            # Get the parent planet's period from planet_data
            parent_period = next(p[4] for p in planet_data if p[0] == parent)
            
            # Find the moon's period from moon_data
            moon_period = next(m[5] for m in moon_data if m[0] == parent and m[1] == name)
            
            # Moon rotations must be added as UpdateFromFunc to follow their planets
            # First create the planet's animation to use as reference
            parent_rotation = Rotating(
                parent_planet,
                angle=max_run_time * (365 / parent_period) * 2 * PI,
                about_point=ORIGIN,
                axis=UP,
                run_time=max_run_time,
                rate_func=linear
            )
            
            # Add the moon's rotation around its planet (higher rotation rate)
            moon_rotation = Rotating(
                moon,
                angle=max_run_time * (30 / moon_period) * 2 * PI,
                about_point=parent_planet.get_center(),
                axis=UP,
                run_time=max_run_time,
                rate_func=linear
            )
            
            # Add moon animation
            moon_animations.append(moon_rotation)
        
        # Add text labels for celestial bodies
        labels = {}
        for name in celestial_bodies:
            if name != "Sun":  # Add labels for planets but not Sun
                label = Text(name, font_size=16)
                label.next_to(celestial_bodies[name], UP * 0.5)
                labels[name] = label
                self.add(label)
        
        # Update function to keep labels with planets
        def update_labels(dt):
            for name, label in labels.items():
                planet = celestial_bodies[name]
                label.next_to(planet, UP * 0.5)
        
        # Play planet animations with labels updating
        self.add_updater(update_labels)
        
        # Play all animations simultaneously
        self.play(*(animations + moon_animations))
        self.wait(2)


# To run this extended scene, use:
# manim -pql extension_example.py ExtendedSolarSystemScene 