import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { ARButton } from 'three/examples/jsm/webxr/ARButton.js';

let scene, camera, renderer, model;
const canvas = document.querySelector('#glCanvas');

function init() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 1.6, 3);

    renderer = new THREE.WebGLRenderer({ antialias: true, canvas: canvas });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.xr.enabled = true;

    const ambientLight = new THREE.HemisphereLight(0xffffff, 0xbbbbff, 1);
    scene.add(ambientLight);

    const loader = new GLTFLoader();
    loader.load('Streetch.glb', function (gltf) {
        model = gltf.scene;
        model.scale.set(0.5, 0.5, 0.5);  // Scale the model down if it's too large
        scene.add(model);
    });

    const arButton = ARButton.createButton(renderer);
    document.body.appendChild(arButton);
    document.getElementById('arButton').style.display = 'block';
    document.getElementById('arButton').onclick = () => {
        document.body.appendChild(ARButton.createButton(renderer, { requiredFeatures: ['hit-test'] }));
    };

    renderer.setAnimationLoop(render);
}

function render() {
    renderer.render(scene, camera);
}

init();
