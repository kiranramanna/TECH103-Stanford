// Module for loading and applying planet textures
import * as THREE from 'three';

export function loadPlanetTextures(textureLoader) {
  // Object to store all loaded textures
  const textures = {};
  
  // Earth texture (we've already downloaded this one)
  textures.earth = {
    map: textureLoader.load('./textures/earth.jpg'),
    bumpMap: null,
    specularMap: null
  };
  
  // Define URLs for other planet textures - these would need to be downloaded separately
  const textureURLs = {
    mercury: 'https://space-assets.ams3.cdn.digitaloceanspaces.com/mercury.jpg',
    venus: 'https://space-assets.ams3.cdn.digitaloceanspaces.com/venus.jpg',
    mars: 'https://space-assets.ams3.cdn.digitaloceanspaces.com/mars.jpg',
    jupiter: 'https://space-assets.ams3.cdn.digitaloceanspaces.com/jupiter.jpg',
    saturn: 'https://space-assets.ams3.cdn.digitaloceanspaces.com/saturn.jpg',
    uranus: 'https://space-assets.ams3.cdn.digitaloceanspaces.com/uranus.jpg',
    neptune: 'https://space-assets.ams3.cdn.digitaloceanspaces.com/neptune.jpg'
  };
  
  // Function to apply textures to a planet mesh
  function applyTextureToPlanet(planet, textureName) {
    if (textures[textureName] && textures[textureName].map) {
      // Create a new material with the texture
      const material = new THREE.MeshPhongMaterial({
        map: textures[textureName].map,
        bumpMap: textures[textureName].bumpMap,
        bumpScale: 0.05,
        specularMap: textures[textureName].specularMap
      });
      
      // Apply the material to the planet
      planet.material = material;
    }
  }
  
  // Example of how to use this - uncomment if you want to pre-load all textures
  /* 
  // Load all planet textures
  Object.keys(textureURLs).forEach(planet => {
    textures[planet] = {
      map: textureLoader.load(textureURLs[planet])
    };
  });
  */
  
  return {
    textures,
    applyTextureToPlanet,
    textureURLs
  };
} 