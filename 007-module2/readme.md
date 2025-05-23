# 3D Solar System Visualization (Web-Based)

This repository provides a lightweight, browser-based 3D solar system model using vanilla HTML, ES6 JavaScript, and Three.js for real-time 3D rendering. No heavy frameworks or build tools required.

## Features

* Interactive 3D visualization of our solar system
* Realistic orbital mechanics and planetary movement
* Customizable planet sizes, distances, and speeds
* Camera controls for zooming, panning, and rotation
* Responsive design that works across devices

## Tech Stack

* **HTML5 & ES6 JavaScript**: Modular, modern JS without a build step
* **Three.js**: Core 3D graphics library for rendering planets and orbits in the browser
* **OrbitControls**: Three.js utility for interactive camera movement
* **Optional texture mapping**: Support for realistic planet textures
* **Optional Analytics**: Integration options for privacy-first metrics
* **Optional Payments**: Support for Stripe Checkout for donations/premium features

## Prerequisites

* A modern web browser (Chrome, Firefox, Safari, Edge)
* (Optional) Node.js & npm for running a local dev server

## Installation & Development

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/3d-solar-system.git
   cd 3d-solar-system
   ```

2. **Run locally**

   * **Without Node**: Simply open `index.html` directly in your browser
   * **With local server** (recommended for texture loading):

     ```bash
     # Using npm
     npm install -g http-server
     http-server -c-1 .
     
     # OR using Python
     python -m http.server 8080
     ```

   Visit `http://localhost:8080` to view the visualization

## Usage

* **Rotate**: Click and drag to rotate the view
* **Zoom**: Scroll to zoom in and out
* **Pan**: Right-click (or Ctrl+click) and drag to pan
* **Reset View**: Double-click to reset camera position

## Example Code Snippet (`index.html`)
UI screen should look like this:

+----------------+-----------------------------+----------------+
|                |                             |                |
|   Left Panel   |         Center Panel       |   Right Panel  |
| (Place, Date & Time)  |     (3D Solar System)       |   (Chat Bot)   |
|                |                             |                |
+----------------+-----------------------------+----------------+

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>3D Solar System</title>
  <style>body { margin: 0; overflow: hidden; background-color: black; }</style>
  <script src="https://unpkg.com/three@0.160.0/build/three.min.js"></script>
</head>
<body>
  <script type="module">
    import { OrbitControls } from 'https://unpkg.com/three@0.160.0/examples/jsm/controls/OrbitControls.js';

    // Scene setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 10, 30);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0x333333);
    scene.add(ambientLight);
    const pointLight = new THREE.PointLight(0xffffff, 2, 100);
    scene.add(pointLight);

    // Sun
    const sun = new THREE.Mesh(
      new THREE.SphereGeometry(2, 32, 32),
      new THREE.MeshBasicMaterial({ color: 0xffff00 })
    );
    scene.add(sun);

    // Planet definitions: [distance, radius, color, speed, inclination]
    const planets = [
      [4, 0.3, 0xaaaaaa, 0.02, 0.03],    // Mercury
      [6, 0.5, 0xffcc00, 0.015, 0.02],   // Venus
      [8, 0.55, 0x3366ff, 0.01, 0],      // Earth
      [10, 0.4, 0xff3300, 0.008, 0.01],  // Mars
      [14, 1.2, 0xffcc99, 0.006, 0.005], // Jupiter
      [18, 1.0, 0xf0c070, 0.005, 0.007], // Saturn
    ];

    const objects = planets.map(([dist, r, color, speed, incl]) => {
      const mesh = new THREE.Mesh(
        new THREE.SphereGeometry(r, 24, 24),
        new THREE.MeshStandardMaterial({ color })
      );
      mesh.userData = { distance: dist, speed, inclination: incl };
      scene.add(mesh);
      return mesh;
    });

    // Controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Render loop
    function animate() {
      requestAnimationFrame(animate);

      // Update planet positions
      const time = Date.now() * 0.0005;
      objects.forEach(obj => {
        const { distance, speed, inclination } = obj.userData;
        obj.position.set(
          Math.cos(time * speed) * distance,
          Math.sin(time * speed) * inclination * distance,
          Math.sin(time * speed) * distance
        );
      });

      controls.update();
      renderer.render(scene, camera);
    }
    animate();

    // Handle resize
    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });
  </script>
</body>
</html>
```

## Customization

### Adding Planet Textures

```javascript
// Load texture maps
const textureLoader = new THREE.TextureLoader();
const earthTexture = textureLoader.load('textures/earth.jpg');
const earthMaterial = new THREE.MeshPhongMaterial({ map: earthTexture });

// Create Earth with texture
const earth = new THREE.Mesh(
  new THREE.SphereGeometry(0.55, 32, 32),
  earthMaterial
);
```

### Adding Orbit Lines

```javascript
// Create orbit visualization
function createOrbit(radius) {
  const orbitGeometry = new THREE.BufferGeometry();
  const points = [];
  
  for (let i = 0; i <= 64; i++) {
    const angle = (i / 64) * Math.PI * 2;
    points.push(new THREE.Vector3(Math.cos(angle) * radius, 0, Math.sin(angle) * radius));
  }
  
  orbitGeometry.setFromPoints(points);
  
  const orbitMaterial = new THREE.LineBasicMaterial({ color: 0x444444, transparent: true, opacity: 0.3 });
  const orbit = new THREE.Line(orbitGeometry, orbitMaterial);
  
  return orbit;
}

// Add orbits for each planet
planets.forEach(([distance]) => {
  scene.add(createOrbit(distance));
});
```

## Advanced Features

* **Asteroid Belt**: Add a particle system between Mars and Jupiter
* **Planet Rings**: Create Saturn's rings using custom geometry
* **Moon Systems**: Add moons orbiting the planets
* **Star Background**: Add a skybox with stars for a more immersive experience
* **Interactive UI**: Add controls to speed up/slow down time, focus on planets, etc.

## Contributing

Contributions are welcome! Open issues or PRs to:

* Improve visuals or interactivity
* Add celestial features like asteroid belts, moons, or comets
* Optimize performance for mobile devices
* Add educational overlays with planet information

## License

MIT License — see [LICENSE](LICENSE) for details.

---

Happy exploring the cosmos!
