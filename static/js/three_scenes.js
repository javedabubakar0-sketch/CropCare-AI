/**
 * CropCare AI - Realistic 3D Botanical & Agricultural Visualizations
 * Built using Three.js (local-first, lightweight, offline-ready).
 *
 * Implements:
 * 1. 3D Botanical Hero (Wheat plant with natural foliar geometry, organic soil clod, wind sway)
 * 2. 3D Interactive Crop-Field Parcel (Connected to SQLite saved farm crops)
 * 3. 3D Foliage Diagnostic Specimen & Optical Scanner (Illustrative guidance)
 * 4. Performance optimization (IntersectionObserver, tab-awareness, prefers-reduced-motion)
 */

(function () {
    "use strict";

    // -------------------------------------------------------------
    // Utility & Capability Checks
    // -------------------------------------------------------------
    function isWebGLSupported() {
        try {
            if (typeof THREE === "undefined") return false;
            const canvas = document.createElement("canvas");
            return !!(window.WebGLRenderingContext && (canvas.getContext("webgl") || canvas.getContext("experimental-webgl")));
        } catch (e) {
            return false;
        }
    }

    function isReducedMotionPreferred() {
        return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    }

    const state = {
        webglAvailable: false,
        activeTab: "tab-dashboard",
        hero: null,
        field: null,
        scanner: null
    };

    // -------------------------------------------------------------
    // Custom Smooth Orbit / Pointer Controller (Zero-Dependency)
    // -------------------------------------------------------------
    function createPointerDragController(domElement, options = {}) {
        const minPolar = options.minPolar !== undefined ? options.minPolar : 0.2;
        const maxPolar = options.maxPolar !== undefined ? options.maxPolar : 1.4;
        const initialPolar = options.initialPolar !== undefined ? options.initialPolar : 0.85;
        const initialAzimuth = options.initialAzimuth !== undefined ? options.initialAzimuth : 0.3;
        const autoRotateSpeed = options.autoRotateSpeed !== undefined ? options.autoRotateSpeed : 0.003;

        let isDown = false;
        let lastX = 0;
        let lastY = 0;
        let targetAzimuth = initialAzimuth;
        let targetPolar = initialPolar;
        let currentAzimuth = initialAzimuth;
        let currentPolar = initialPolar;
        let userInteracting = false;
        let idleTimer = 0;

        function onPointerDown(e) {
            isDown = true;
            userInteracting = true;
            idleTimer = 0;
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            lastX = clientX;
            lastY = clientY;
            if (e.target && e.target.setPointerCapture && e.pointerId) {
                try { e.target.setPointerCapture(e.pointerId); } catch (_) {}
            }
        }

        function onPointerMove(e) {
            if (!isDown) return;
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            const dx = clientX - lastX;
            const dy = clientY - lastY;
            lastX = clientX;
            lastY = clientY;

            targetAzimuth += dx * 0.008;
            targetPolar += dy * 0.006;
            targetPolar = Math.max(minPolar, Math.min(maxPolar, targetPolar));
            idleTimer = 0;
        }

        function onPointerUp(e) {
            isDown = false;
            setTimeout(() => { userInteracting = false; }, 800);
        }

        domElement.style.touchAction = "none";
        domElement.addEventListener("pointerdown", onPointerDown, { passive: true });
        window.addEventListener("pointermove", onPointerMove, { passive: true });
        window.addEventListener("pointerup", onPointerUp, { passive: true });
        domElement.addEventListener("touchstart", onPointerDown, { passive: true });
        window.addEventListener("touchmove", onPointerMove, { passive: true });
        window.addEventListener("touchend", onPointerUp, { passive: true });

        return {
            update(autoRotate = true) {
                if (autoRotate && !isDown && !userInteracting && !isReducedMotionPreferred()) {
                    targetAzimuth += autoRotateSpeed;
                }
                currentAzimuth += (targetAzimuth - currentAzimuth) * 0.08;
                currentPolar += (targetPolar - currentPolar) * 0.08;
                return { azimuth: currentAzimuth, polar: currentPolar };
            },
            reset(az = initialAzimuth, pol = initialPolar) {
                targetAzimuth = az;
                targetPolar = pol;
            },
            setAzimuth(az) { targetAzimuth = az; },
            setPolar(pol) { targetPolar = Math.max(minPolar, Math.min(maxPolar, pol)); }
        };
    }

    // -------------------------------------------------------------
    // SCENE 1: 3D Wheat Hero Specimen & Soil Mound
    // -------------------------------------------------------------
    function initHeroWheatScene() {
        const container = document.getElementById("hero-3d-canvas-container");
        if (!container) return null;

        const width = container.clientWidth || 480;
        const height = container.clientHeight || 420;

        // Scene, Camera, Renderer
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(36, width / height, 0.1, 50);
        camera.position.set(0, 1.8, 5.2);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: "default" });
        renderer.setSize(width, height);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.05;
        container.innerHTML = "";
        container.appendChild(renderer.domElement);

        // Lighting
        const hemiLight = new THREE.HemisphereLight(0xf4fbf7, 0x3d3023, 0.85);
        scene.add(hemiLight);

        const sunLight = new THREE.DirectionalLight(0xfffaed, 1.35);
        sunLight.position.set(3.5, 6.0, 3.8);
        sunLight.castShadow = true;
        sunLight.shadow.mapSize.width = 1024;
        sunLight.shadow.mapSize.height = 1024;
        sunLight.shadow.camera.near = 0.5;
        sunLight.shadow.camera.far = 15;
        sunLight.shadow.camera.left = -2.5;
        sunLight.shadow.camera.right = 2.5;
        sunLight.shadow.camera.top = 2.5;
        sunLight.shadow.camera.bottom = -2.5;
        sunLight.shadow.bias = -0.0005;
        scene.add(sunLight);

        const rimLight = new THREE.DirectionalLight(0xbbf7d0, 0.4);
        rimLight.position.set(-3.0, 3.0, -2.5);
        scene.add(rimLight);

        // Soil Mound (Loam clod with organic crumb)
        const soilGroup = new THREE.Group();
        const soilRadius = 1.6;
        const soilGeo = new THREE.CylinderGeometry(1.4, 1.7, 0.65, 32, 4);
        const pos = soilGeo.attributes.position;
        for (let i = 0; i < pos.count; i++) {
            const y = pos.getY(i);
            const x = pos.getX(i);
            const z = pos.getZ(i);
            if (y > 0) {
                // Round top mound with organic variance
                const dist = Math.sqrt(x * x + z * z);
                const bump = Math.sin(x * 6.0) * Math.cos(z * 6.0) * 0.05 + Math.sin(x * 12.0) * 0.02;
                pos.setY(i, y + (1.0 - Math.min(1.0, dist / 1.5)) * 0.35 + bump);
            }
        }
        soilGeo.computeVertexNormals();

        const soilMat = new THREE.MeshStandardMaterial({
            color: 0x3a291b,
            roughness: 0.95,
            metalness: 0.05,
            flatShading: true
        });
        const soilMesh = new THREE.Mesh(soilGeo, soilMat);
        soilMesh.position.y = -0.3;
        soilMesh.receiveShadow = true;
        soilMesh.castShadow = true;
        soilGroup.add(soilMesh);

        // Soil Crumbs & Small Pebbles
        const pebbleGeo = new THREE.DodecahedronGeometry(0.06, 0);
        const pebbleMat = new THREE.MeshStandardMaterial({ color: 0x4f3d2e, roughness: 0.9 });
        for (let i = 0; i < 18; i++) {
            const pebble = new THREE.Mesh(pebbleGeo, pebbleMat);
            const angle = (i / 18) * Math.PI * 2 + Math.random() * 0.2;
            const dist = 0.5 + Math.random() * 0.9;
            pebble.position.set(Math.cos(angle) * dist, 0.05 + Math.random() * 0.04, Math.sin(angle) * dist);
            pebble.scale.set(0.6 + Math.random() * 0.8, 0.4 + Math.random() * 0.6, 0.6 + Math.random() * 0.8);
            pebble.rotation.set(Math.random(), Math.random(), Math.random());
            pebble.castShadow = true;
            soilGroup.add(pebble);
        }

        // Contact Shadow Plane
        const shadowPlaneGeo = new THREE.PlaneGeometry(4.2, 4.2);
        const canvasShadow = document.createElement("canvas");
        canvasShadow.width = 128;
        canvasShadow.height = 128;
        const ctxShadow = canvasShadow.getContext("2d");
        const grad = ctxShadow.createRadialGradient(64, 64, 10, 64, 64, 60);
        grad.addColorStop(0, "rgba(20, 28, 22, 0.55)");
        grad.addColorStop(0.5, "rgba(20, 28, 22, 0.22)");
        grad.addColorStop(1, "rgba(20, 28, 22, 0)");
        ctxShadow.fillStyle = grad;
        ctxShadow.fillRect(0, 0, 128, 128);
        const shadowTex = new THREE.CanvasTexture(canvasShadow);
        const shadowMat = new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, opacity: 0.75, depthWrite: false });
        const shadowMesh = new THREE.Mesh(shadowPlaneGeo, shadowMat);
        shadowMesh.rotation.x = -Math.PI / 2;
        shadowMesh.position.y = -0.63;
        soilGroup.add(shadowMesh);

        scene.add(soilGroup);

        // ---------------------------------------------------------
        // Procedural Wheat Plant Model (Tillers, Leaves, Awned Head)
        // ---------------------------------------------------------
        const plantRoot = new THREE.Group();
        plantRoot.position.y = 0.05;
        scene.add(plantRoot);

        // Materials
        const stemMat = new THREE.MeshStandardMaterial({
            color: 0x588746,
            roughness: 0.62,
            metalness: 0.08
        });

        const nodeMat = new THREE.MeshStandardMaterial({
            color: 0x7a9c4d,
            roughness: 0.55,
            metalness: 0.08
        });

        const leafMat = new THREE.MeshStandardMaterial({
            color: 0x487a3d,
            roughness: 0.68,
            metalness: 0.04,
            side: THREE.DoubleSide
        });

        const spikeMat = new THREE.MeshStandardMaterial({
            color: 0x989a54,
            roughness: 0.58,
            metalness: 0.1
        });

        const awnMat = new THREE.MeshStandardMaterial({
            color: 0xbdb96e,
            roughness: 0.5
        });

        // Tiller references for dynamic wind animation
        const animatedTillers = [];
        const animatedLeaves = [];
        let headingSpikeGroup = null;

        // Leaf Generator: Curved strap-like blade with central vein groove
        function createWheatLeaf(length, maxWidth, archAngle, droopStrength) {
            const segmentsU = 8;
            const segmentsV = 22;
            const geo = new THREE.PlaneGeometry(maxWidth, length, segmentsU, segmentsV);
            const p = geo.attributes.position;

            for (let i = 0; i < p.count; i++) {
                const y = p.getY(i); // ranges from -length/2 to +length/2
                const normY = (y + length / 2) / length; // 0 at base, 1 at tip
                const x = p.getX(i);

                // Taper width from base to tip
                const taper = Math.sin(normY * Math.PI * 0.92);
                p.setX(i, x * Math.max(0.08, taper));

                // Natural arch and gravitational droop along Y
                const curveZ = -Math.pow(normY, 2.2) * droopStrength * length;
                // V-shaped groove down central midrib
                const midribGroove = -Math.abs(x / maxWidth) * 0.02 * (1 - normY);
                p.setZ(i, curveZ + midribGroove);

                // Shift origin to leaf attachment base
                p.setY(i, normY * length);
            }
            geo.computeVertexNormals();

            const leafMesh = new THREE.Mesh(geo, leafMat);
            leafMesh.castShadow = true;
            leafMesh.receiveShadow = true;
            return leafMesh;
        }

        // Wheat Spike (Ear) with overlapping spikelets & long slender awns
        function createAwnedWheatSpike(spikeLength = 0.85) {
            const spikeGroup = new THREE.Group();
            const spikeletsCount = 14;
            const spikeletGeo = new THREE.ConeGeometry(0.05, 0.14, 6);
            spikeletGeo.rotateX(Math.PI);

            const awnGeo = new THREE.CylinderGeometry(0.004, 0.001, 0.45, 4);
            awnGeo.translate(0, 0.22, 0);

            for (let i = 0; i < spikeletsCount; i++) {
                const t = i / spikeletsCount;
                const y = t * spikeLength;
                const side = (i % 2 === 0) ? 1 : -1;
                const angle = (i % 2 === 0) ? 0.35 : -0.35;

                const spikelet = new THREE.Mesh(spikeletGeo, spikeMat);
                spikelet.position.set(side * 0.038, y, (Math.random() - 0.5) * 0.015);
                spikelet.rotation.z = angle;
                spikelet.rotation.y = side * 0.2;
                spikelet.castShadow = true;
                spikeGroup.add(spikelet);

                // Awn (long bristle projecting upwards)
                const awn = new THREE.Mesh(awnGeo, awnMat);
                awn.position.copy(spikelet.position);
                awn.rotation.z = angle * 0.85 + (side * 0.15);
                awn.rotation.x = (Math.random() - 0.5) * 0.15;
                awn.castShadow = true;
                spikeGroup.add(awn);
            }

            // Rachis (central spike stem)
            const rachisGeo = new THREE.CylinderGeometry(0.018, 0.022, spikeLength, 8);
            rachisGeo.translate(0, spikeLength / 2, 0);
            const rachis = new THREE.Mesh(rachisGeo, stemMat);
            rachis.castShadow = true;
            spikeGroup.add(rachis);

            return spikeGroup;
        }

        // Build Primary Main Culm (Stem + Leaves + Head)
        function buildPrimaryCulm() {
            const culmGroup = new THREE.Group();

            // Lower Stem (Internode 1)
            const stem1Geo = new THREE.CylinderGeometry(0.032, 0.038, 0.65, 10);
            stem1Geo.translate(0, 0.325, 0);
            const stem1 = new THREE.Mesh(stem1Geo, stemMat);
            stem1.castShadow = true;
            culmGroup.add(stem1);

            // Node 1
            const node1Geo = new THREE.TorusGeometry(0.035, 0.009, 6, 12);
            node1Geo.rotateX(Math.PI / 2);
            const node1 = new THREE.Mesh(node1Geo, nodeMat);
            node1.position.y = 0.65;
            culmGroup.add(node1);

            // Leaf 1
            const leaf1 = createWheatLeaf(0.9, 0.08, 0.7, 0.45);
            leaf1.position.set(0, 0.65, 0);
            leaf1.rotation.set(0.4, 0.3, 0.55);
            culmGroup.add(leaf1);
            animatedLeaves.push({ mesh: leaf1, baseRotZ: 0.55, phase: 0.2, freq: 1.1, flutter: 0.05 });

            // Mid Stem (Internode 2)
            const midJoint = new THREE.Group();
            midJoint.position.y = 0.65;

            const stem2Geo = new THREE.CylinderGeometry(0.027, 0.032, 0.75, 10);
            stem2Geo.translate(0, 0.375, 0);
            const stem2 = new THREE.Mesh(stem2Geo, stemMat);
            stem2.castShadow = true;
            midJoint.add(stem2);

            // Node 2
            const node2 = new THREE.Mesh(node1Geo, nodeMat);
            node2.position.y = 0.75;
            midJoint.add(node2);

            // Leaf 2 (opposite direction)
            const leaf2 = createWheatLeaf(1.15, 0.09, 0.65, 0.5);
            leaf2.position.set(0, 0.75, 0);
            leaf2.rotation.set(-0.35, 2.8, -0.6);
            midJoint.add(leaf2);
            animatedLeaves.push({ mesh: leaf2, baseRotZ: -0.6, phase: 1.1, freq: 1.2, flutter: 0.06 });

            // Upper Stem (Peduncle / Flag Leaf Joint)
            const upperJoint = new THREE.Group();
            upperJoint.position.y = 0.75;

            const stem3Geo = new THREE.CylinderGeometry(0.022, 0.027, 0.85, 10);
            stem3Geo.translate(0, 0.425, 0);
            const stem3 = new THREE.Mesh(stem3Geo, stemMat);
            stem3.castShadow = true;
            upperJoint.add(stem3);

            // Flag Leaf (Uppermost photosynthetic leaf nourishing the grain)
            const flagLeaf = createWheatLeaf(0.85, 0.075, 0.5, 0.38);
            flagLeaf.position.set(0, 0.5, 0);
            flagLeaf.rotation.set(0.3, 1.2, 0.45);
            upperJoint.add(flagLeaf);
            animatedLeaves.push({ mesh: flagLeaf, baseRotZ: 0.45, phase: 2.3, freq: 1.4, flutter: 0.08 });

            // Heading Wheat Ear at top
            headingSpikeGroup = createAwnedWheatSpike(0.78);
            headingSpikeGroup.position.set(0, 0.85, 0);
            upperJoint.add(headingSpikeGroup);

            midJoint.add(upperJoint);
            culmGroup.add(midJoint);

            animatedTillers.push({
                root: culmGroup,
                mid: midJoint,
                top: upperJoint,
                head: headingSpikeGroup,
                phaseOffset: 0.0
            });

            return culmGroup;
        }

        // Secondary Tiller 1 (Younger, angled tiller)
        function buildSecondaryTiller(angleY, tiltZ, scale) {
            const tiller = new THREE.Group();
            tiller.rotation.y = angleY;
            tiller.rotation.z = tiltZ;
            tiller.scale.set(scale, scale, scale);

            const stemGeo = new THREE.CylinderGeometry(0.024, 0.03, 1.1, 8);
            stemGeo.translate(0, 0.55, 0);
            const stem = new THREE.Mesh(stemGeo, stemMat);
            stem.castShadow = true;
            tiller.add(stem);

            const leafA = createWheatLeaf(0.8, 0.07, 0.6, 0.45);
            leafA.position.set(0, 0.45, 0);
            leafA.rotation.set(0.3, 0.4, 0.5);
            tiller.add(leafA);
            animatedLeaves.push({ mesh: leafA, baseRotZ: 0.5, phase: 0.7, freq: 1.2, flutter: 0.06 });

            const leafB = createWheatLeaf(0.95, 0.075, 0.55, 0.48);
            leafB.position.set(0, 0.85, 0);
            leafB.rotation.set(-0.25, -2.5, -0.55);
            tiller.add(leafB);
            animatedLeaves.push({ mesh: leafB, baseRotZ: -0.55, phase: 1.6, freq: 1.3, flutter: 0.07 });

            // Small emerging ear
            const smallSpike = createAwnedWheatSpike(0.5);
            smallSpike.position.set(0, 1.1, 0);
            smallSpike.scale.set(0.75, 0.75, 0.75);
            tiller.add(smallSpike);

            animatedTillers.push({
                root: tiller,
                mid: tiller,
                top: smallSpike,
                head: smallSpike,
                phaseOffset: angleY * 0.5
            });

            return tiller;
        }

        const mainCulm = buildPrimaryCulm();
        plantRoot.add(mainCulm);

        const tiller1 = buildSecondaryTiller(1.4, 0.14, 0.88);
        plantRoot.add(tiller1);

        const tiller2 = buildSecondaryTiller(-1.9, 0.16, 0.82);
        plantRoot.add(tiller2);

        // Subtle root collar / base sheath
        const collarGeo = new THREE.ConeGeometry(0.12, 0.18, 8);
        const collar = new THREE.Mesh(collarGeo, stemMat);
        collar.position.y = 0.04;
        plantRoot.add(collar);

        // Pointer controls
        const controls = createPointerDragController(renderer.domElement, {
            initialAzimuth: 0.4,
            initialPolar: 0.95,
            minPolar: 0.35,
            maxPolar: 1.35,
            autoRotateSpeed: 0.0025
        });

        // Wind simulation parameters
        let windStrength = 1.0; // 0: Calm, 1: Gentle Breeze (8 km/h), 2: Field Wind (18 km/h)
        let growthStage = "heading"; // "heading" or "tillering"
        let isRunning = true;
        let clock = new THREE.Clock();

        function applyGrowthStage(stage) {
            growthStage = stage;
            if (stage === "tillering") {
                // Young vegetative wheat: hide mature grain spike, keep lush green tillers
                if (headingSpikeGroup) headingSpikeGroup.visible = false;
                plantRoot.scale.set(1.0, 0.82, 1.0);
            } else {
                // Heading stage: full spike visible
                if (headingSpikeGroup) headingSpikeGroup.visible = true;
                plantRoot.scale.set(1.0, 1.0, 1.0);
            }
        }

        function setWindVelocity(mode) {
            if (mode === "calm") windStrength = 0.15;
            else if (mode === "field") windStrength = 2.2;
            else windStrength = 1.0; // gentle
        }

        // Render loop with harmonic wind sway
        function animate() {
            if (!isRunning) return;
            requestAnimationFrame(animate);

            const delta = clock.getDelta();
            const elapsed = clock.getElapsedTime();

            // Update Orbit Camera
            const { azimuth, polar } = controls.update(true);
            const radius = 5.0;
            camera.position.x = radius * Math.sin(polar) * Math.sin(azimuth);
            camera.position.z = radius * Math.sin(polar) * Math.cos(azimuth);
            camera.position.y = 0.75 + radius * Math.cos(polar);
            camera.lookAt(0, 0.95, 0);

            // Natural Wind Harmonic Sway
            if (!isReducedMotionPreferred()) {
                const windTime = elapsed * (1.2 + windStrength * 0.8);
                const windAmp = 0.035 * windStrength;

                animatedTillers.forEach(t => {
                    const wave1 = Math.sin(windTime + t.phaseOffset);
                    const wave2 = Math.cos(windTime * 0.7 + t.phaseOffset);

                    if (t.mid) {
                        t.mid.rotation.z = wave1 * windAmp * 0.6;
                        t.mid.rotation.x = wave2 * windAmp * 0.4;
                    }
                    if (t.top) {
                        t.top.rotation.z = Math.sin(windTime * 1.3 + t.phaseOffset) * windAmp * 1.1;
                        t.top.rotation.x = Math.cos(windTime * 1.1 + t.phaseOffset) * windAmp * 0.7;
                    }
                });

                // Subtle leaf blade flutter
                animatedLeaves.forEach(l => {
                    const flutter = Math.sin(windTime * l.freq + l.phase) * (l.flutter * windStrength);
                    l.mesh.rotation.z = l.baseRotZ + flutter;
                });
            }

            renderer.render(scene, camera);
        }

        animate();

        // Responsive resize
        function onResize() {
            if (!container) return;
            const w = container.clientWidth;
            const h = container.clientHeight || 420;
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
            renderer.setSize(w, h);
        }
        window.addEventListener("resize", onResize, { passive: true });

        // Hook interactive UI controls
        const stageTilleringBtn = document.getElementById("btn-stage-tillering");
        const stageHeadingBtn = document.getElementById("btn-stage-heading");
        if (stageTilleringBtn && stageHeadingBtn) {
            stageTilleringBtn.addEventListener("click", () => {
                stageTilleringBtn.classList.add("active");
                stageHeadingBtn.classList.remove("active");
                applyGrowthStage("tillering");
            });
            stageHeadingBtn.addEventListener("click", () => {
                stageHeadingBtn.classList.add("active");
                stageTilleringBtn.classList.remove("active");
                applyGrowthStage("heading");
            });
        }

        const windPills = document.querySelectorAll("[data-wind-mode]");
        windPills.forEach(pill => {
            pill.addEventListener("click", () => {
                windPills.forEach(p => p.classList.remove("active"));
                pill.classList.add("active");
                const mode = pill.getAttribute("data-wind-mode");
                setWindVelocity(mode);
            });
        });

        const resetBtn = document.getElementById("btn-reset-hero-3d");
        if (resetBtn) {
            resetBtn.addEventListener("click", () => {
                controls.reset(0.4, 0.95);
            });
        }

        return {
            start() {
                if (!isRunning) {
                    isRunning = true;
                    clock.start();
                    animate();
                }
            },
            pause() {
                isRunning = false;
                clock.stop();
            },
            setWindVelocity,
            applyGrowthStage,
            resize: onResize
        };
    }

    // -------------------------------------------------------------
    // SCENE 2: 3D Interactive Crop-Field Parcel
    // -------------------------------------------------------------
    function initFieldScene() {
        const container = document.getElementById("field-3d-canvas-container");
        if (!container) return null;

        const width = container.clientWidth || 640;
        const height = container.clientHeight || 340;

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(38, width / height, 0.1, 50);
        camera.position.set(0, 4.0, 5.8);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(width, height);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        container.innerHTML = "";
        container.appendChild(renderer.domElement);

        // Lighting
        const hemi = new THREE.HemisphereLight(0xfefce8, 0x3d3023, 0.8);
        scene.add(hemi);

        const sun = new THREE.DirectionalLight(0xfffbeb, 1.25);
        sun.position.set(4, 7, 3);
        sun.castShadow = true;
        sun.shadow.mapSize.width = 1024;
        sun.shadow.mapSize.height = 1024;
        scene.add(sun);

        // Ground / Furrowed Field Base (Agricultural parcel)
        const fieldWidth = 6.2;
        const fieldLength = 4.2;
        const baseGeo = new THREE.BoxGeometry(fieldWidth, 0.45, fieldLength);
        const baseMat = new THREE.MeshStandardMaterial({
            color: 0x422f20, // Rich dark alluvial soil
            roughness: 0.92,
            metalness: 0.05
        });
        const fieldBase = new THREE.Mesh(baseGeo, baseMat);
        fieldBase.position.y = -0.25;
        fieldBase.receiveShadow = true;
        scene.add(fieldBase);

        // Furrow Ridges (Parallel soil ridges created by tractor / plough)
        const ridgeMat = new THREE.MeshStandardMaterial({ color: 0x4a3625, roughness: 0.95 });
        const ridgeCount = 6;
        for (let r = 0; r < ridgeCount; r++) {
            const z = -fieldLength / 2 + 0.4 + r * 0.65;
            const ridgeGeo = new THREE.CylinderGeometry(0.12, 0.18, fieldWidth - 0.4, 8);
            ridgeGeo.rotateZ(Math.PI / 2);
            const ridge = new THREE.Mesh(ridgeGeo, ridgeMat);
            ridge.position.set(0, 0.02, z);
            ridge.receiveShadow = true;
            ridge.castShadow = true;
            scene.add(ridge);
        }

        // Irrigation Canal / Field Bund Boundary (Water channel)
        const waterGeo = new THREE.BoxGeometry(fieldWidth - 0.4, 0.06, 0.28);
        const waterMat = new THREE.MeshStandardMaterial({
            color: 0x456c7a,
            roughness: 0.2,
            metalness: 0.35,
            transparent: true,
            opacity: 0.82
        });
        const waterChannel = new THREE.Mesh(waterGeo, waterMat);
        waterChannel.position.set(0, -0.01, -fieldLength / 2 + 0.22);
        scene.add(waterChannel);

        // Dynamic Crop Rows Group (Syncs with SQLite saved crops)
        const cropRowsGroup = new THREE.Group();
        scene.add(cropRowsGroup);

        const rowInteractiveMeshes = [];
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();

        // Foliage generators for different Pakistani crops
        function createWheatTuft() {
            const tuft = new THREE.Group();
            const bladeGeo = new THREE.ConeGeometry(0.04, 0.38, 4);
            const mat = new THREE.MeshStandardMaterial({ color: 0x6e944b, roughness: 0.7 });
            for (let i = 0; i < 4; i++) {
                const blade = new THREE.Mesh(bladeGeo, mat);
                blade.rotation.z = (Math.random() - 0.5) * 0.45;
                blade.rotation.x = (Math.random() - 0.5) * 0.45;
                blade.position.set((Math.random() - 0.5) * 0.08, 0.18, (Math.random() - 0.5) * 0.08);
                blade.castShadow = true;
                tuft.add(blade);
            }
            return tuft;
        }

        function createCottonBush() {
            const bush = new THREE.Group();
            const leavesGeo = new THREE.DodecahedronGeometry(0.16, 1);
            const leavesMat = new THREE.MeshStandardMaterial({ color: 0x2e5c36, roughness: 0.8 });
            const foliage = new THREE.Mesh(leavesGeo, leavesMat);
            foliage.position.y = 0.16;
            foliage.castShadow = true;
            bush.add(foliage);

            // Fluffy white cotton bolls
            const bollGeo = new THREE.SphereGeometry(0.04, 6, 6);
            const bollMat = new THREE.MeshStandardMaterial({ color: 0xfafafa, roughness: 0.95 });
            for (let b = 0; b < 3; b++) {
                const boll = new THREE.Mesh(bollGeo, bollMat);
                boll.position.set((Math.random() - 0.5) * 0.22, 0.14 + Math.random() * 0.12, (Math.random() - 0.5) * 0.22);
                bush.add(boll);
            }
            return bush;
        }

        function createTomatoRowPlant() {
            const plant = new THREE.Group();
            const leavesGeo = new THREE.SphereGeometry(0.18, 7, 7);
            const leavesMat = new THREE.MeshStandardMaterial({ color: 0x3d7843, roughness: 0.75 });
            const foliage = new THREE.Mesh(leavesGeo, leavesMat);
            foliage.position.y = 0.18;
            foliage.scale.set(1.1, 0.85, 1.0);
            foliage.castShadow = true;
            plant.add(foliage);

            // Red tomato sphere
            const fruitGeo = new THREE.SphereGeometry(0.045, 6, 6);
            const fruitMat = new THREE.MeshStandardMaterial({ color: 0xc92a2a, roughness: 0.4 });
            const fruit = new THREE.Mesh(fruitGeo, fruitMat);
            fruit.position.set(0.1, 0.12, 0.1);
            plant.add(fruit);
            return plant;
        }

        function createCornStalk() {
            const corn = new THREE.Group();
            const stalkGeo = new THREE.CylinderGeometry(0.02, 0.025, 0.65, 6);
            stalkGeo.translate(0, 0.32, 0);
            const stalkMat = new THREE.MeshStandardMaterial({ color: 0x5b8a3e, roughness: 0.65 });
            const stalk = new THREE.Mesh(stalkGeo, stalkMat);
            stalk.castShadow = true;
            corn.add(stalk);

            const bladeGeo = new THREE.PlaneGeometry(0.08, 0.35);
            const bladeMat = new THREE.MeshStandardMaterial({ color: 0x487a32, side: THREE.DoubleSide });
            const b1 = new THREE.Mesh(bladeGeo, bladeMat);
            b1.position.set(0, 0.32, 0);
            b1.rotation.set(0.4, 0, 0.6);
            corn.add(b1);
            return corn;
        }

        function createGenericPlant() {
            const group = new THREE.Group();
            const geo = new THREE.SphereGeometry(0.15, 6, 6);
            const mat = new THREE.MeshStandardMaterial({ color: 0x4a7a40, roughness: 0.8 });
            const m = new THREE.Mesh(geo, mat);
            m.position.y = 0.15;
            m.castShadow = true;
            group.add(m);
            return group;
        }

        // Populate 3D Field Rows based on saved SQLite crops
        function updateCropsInScene(cropsList) {
            // Clear existing rows
            while (cropRowsGroup.children.length > 0) {
                cropRowsGroup.remove(cropRowsGroup.children[0]);
            }
            rowInteractiveMeshes.length = 0;

            const tooltipEl = document.getElementById("field-3d-tooltip");
            if (tooltipEl) tooltipEl.style.display = "none";

            if (!cropsList || cropsList.length === 0) {
                // Render Empty Ploughed Field Sign
                const signGroup = new THREE.Group();
                const poleGeo = new THREE.CylinderGeometry(0.03, 0.03, 0.9, 6);
                poleGeo.translate(0, 0.45, 0);
                const woodMat = new THREE.MeshStandardMaterial({ color: 0x6e5239, roughness: 0.85 });
                const pole = new THREE.Mesh(poleGeo, woodMat);
                signGroup.add(pole);

                const boardGeo = new THREE.BoxGeometry(1.6, 0.5, 0.06);
                boardGeo.translate(0, 0.72, 0);
                const boardMat = new THREE.MeshStandardMaterial({ color: 0x8a6948, roughness: 0.8 });
                const board = new THREE.Mesh(boardGeo, boardMat);
                signGroup.add(board);
                signGroup.position.set(0, 0.05, 0);
                cropRowsGroup.add(signGroup);
                return;
            }

            // Map registered crops onto furrow rows
            const maxRows = Math.min(cropsList.length, 5);
            for (let i = 0; i < maxRows; i++) {
                const crop = cropsList[i];
                const z = -fieldLength / 2 + 0.75 + i * 0.75;
                const rowGroup = new THREE.Group();
                rowGroup.position.set(0, 0.08, z);

                // Invisible interaction hit-box for raycasting
                const hitBoxGeo = new THREE.BoxGeometry(fieldWidth - 0.5, 0.7, 0.65);
                const hitBoxMat = new THREE.MeshBasicMaterial({ visible: false });
                const hitBox = new THREE.Mesh(hitBoxGeo, hitBoxMat);
                hitBox.userData = { crop: crop, index: i, rowGroup: rowGroup };
                rowGroup.add(hitBox);
                rowInteractiveMeshes.push(hitBox);

                // Plant individual plants along this row
                const plantCount = 9;
                const spacing = (fieldWidth - 1.2) / plantCount;
                const startX = -(fieldWidth - 1.2) / 2;

                const cropType = (crop.crop_name || "").toLowerCase();
                for (let p = 0; p < plantCount; p++) {
                    const x = startX + p * spacing + (Math.random() - 0.5) * 0.05;
                    let plantMesh;
                    if (cropType.includes("wheat") || cropType.includes("گندم")) {
                        plantMesh = createWheatTuft();
                    } else if (cropType.includes("cotton") || cropType.includes("کپاس")) {
                        plantMesh = createCottonBush();
                    } else if (cropType.includes("tomato") || cropType.includes("ٹماٹر")) {
                        plantMesh = createTomatoRowPlant();
                    } else if (cropType.includes("corn") || cropType.includes("maize") || cropType.includes("مکئی")) {
                        plantMesh = createCornStalk();
                    } else {
                        plantMesh = createGenericPlant();
                    }
                    plantMesh.position.set(x, 0, (Math.random() - 0.5) * 0.08);
                    const scaleVar = 0.85 + Math.random() * 0.3;
                    plantMesh.scale.set(scaleVar, scaleVar, scaleVar);
                    rowGroup.add(plantMesh);
                }

                // Field Plot Label Marker
                const markerGeo = new THREE.CylinderGeometry(0.04, 0.04, 0.35, 6);
                markerGeo.translate(0, 0.175, 0);
                const markerMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.3 });
                const marker = new THREE.Mesh(markerGeo, markerMat);
                marker.position.set(-fieldWidth / 2 + 0.3, 0, 0);
                rowGroup.add(marker);

                cropRowsGroup.add(rowGroup);
            }
        }

        // Pointer controls
        const controls = createPointerDragController(renderer.domElement, {
            initialAzimuth: 0.15,
            initialPolar: 0.85,
            minPolar: 0.45,
            maxPolar: 1.15,
            autoRotateSpeed: 0.001
        });

        // Hover & Click interaction
        let hoveredMesh = null;
        const tooltip = document.getElementById("field-3d-tooltip");

        function onPointerMove(e) {
            const rect = renderer.domElement.getBoundingClientRect();
            mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
            mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(rowInteractiveMeshes);

            if (intersects.length > 0) {
                const hit = intersects[0].object;
                if (hoveredMesh !== hit) {
                    if (hoveredMesh) hoveredMesh.userData.rowGroup.position.y = 0.08;
                    hoveredMesh = hit;
                    hoveredMesh.userData.rowGroup.position.y = 0.14; // Subtle lift
                }

                if (tooltip && hit.userData && hit.userData.crop) {
                    const c = hit.userData.crop;
                    tooltip.style.display = "block";
                    tooltip.style.left = `${e.clientX - rect.left + 15}px`;
                    tooltip.style.top = `${e.clientY - rect.top - 15}px`;
                    tooltip.innerHTML = `<strong>${c.crop_name}</strong> &bull; ${c.field_name} (${c.area_acres} Acres)`;
                }
            } else {
                if (hoveredMesh) {
                    hoveredMesh.userData.rowGroup.position.y = 0.08;
                    hoveredMesh = null;
                }
                if (tooltip) tooltip.style.display = "none";
            }
        }

        function onPointerClick(e) {
            if (!hoveredMesh || !hoveredMesh.userData || !hoveredMesh.userData.crop) return;
            const crop = hoveredMesh.userData.crop;
            // Scroll to the fields table and highlight the corresponding row
            const table = document.getElementById("crops-table");
            if (table) {
                table.scrollIntoView({ behavior: "smooth", block: "center" });
                const rows = table.querySelectorAll("tbody tr");
                rows.forEach(tr => {
                    if (tr.textContent.includes(crop.field_name)) {
                        tr.classList.add("highlight-field-row");
                        setTimeout(() => tr.classList.remove("highlight-field-row"), 2500);
                    }
                });
            }
        }

        renderer.domElement.addEventListener("pointermove", onPointerMove, { passive: true });
        renderer.domElement.addEventListener("click", onPointerClick);

        let isRunning = false;
        function animate() {
            if (!isRunning) return;
            requestAnimationFrame(animate);

            const { azimuth, polar } = controls.update(true);
            const radius = 6.2;
            camera.position.x = radius * Math.sin(polar) * Math.sin(azimuth);
            camera.position.z = radius * Math.sin(polar) * Math.cos(azimuth);
            camera.position.y = radius * Math.cos(polar);
            camera.lookAt(0, 0, 0);

            renderer.render(scene, camera);
        }

        function onResize() {
            if (!container) return;
            const w = container.clientWidth;
            const h = container.clientHeight || 340;
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
            renderer.setSize(w, h);
        }
        window.addEventListener("resize", onResize, { passive: true });

        return {
            start() {
                if (!isRunning) {
                    isRunning = true;
                    animate();
                }
            },
            pause() {
                isRunning = false;
            },
            updateCrops: updateCropsInScene,
            resize: onResize
        };
    }

    // -------------------------------------------------------------
    // SCENE 3: 3D Foliage Diagnostic Specimen & Optical Scanner
    // -------------------------------------------------------------
    function initScannerLeafScene() {
        const container = document.getElementById("scanner-3d-canvas-container");
        if (!container) return null;

        const width = container.clientWidth || 360;
        const height = container.clientHeight || 320;

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(34, width / height, 0.1, 50);
        camera.position.set(0, 1.8, 3.8);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(width, height);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        container.innerHTML = "";
        container.appendChild(renderer.domElement);

        // Lighting
        const hemi = new THREE.HemisphereLight(0xf1f8f3, 0x2e3b2e, 0.9);
        scene.add(hemi);

        const spot = new THREE.SpotLight(0xfffaed, 1.4);
        spot.position.set(2, 4.5, 3);
        spot.castShadow = true;
        scene.add(spot);

        // Agronomic Inspection Plate (Stage with calibrated coordinate rings)
        const stageGroup = new THREE.Group();
        const stagePlateGeo = new THREE.CylinderGeometry(1.4, 1.45, 0.1, 36);
        const stagePlateMat = new THREE.MeshStandardMaterial({
            color: 0x24362a, // Dark calibrated lab plate
            roughness: 0.65,
            metalness: 0.2
        });
        const stagePlate = new THREE.Mesh(stagePlateGeo, stagePlateMat);
        stagePlate.position.y = -0.05;
        stagePlate.receiveShadow = true;
        stageGroup.add(stagePlate);

        // Precision Coordinate Rings on stage
        const ringGeo = new THREE.RingGeometry(0.7, 0.72, 36);
        ringGeo.rotateX(-Math.PI / 2);
        const ringMat = new THREE.MeshBasicMaterial({ color: 0x4d6b54, side: THREE.DoubleSide, opacity: 0.6, transparent: true });
        const ring = new THREE.Mesh(ringGeo, ringMat);
        ring.position.y = 0.005;
        stageGroup.add(ring);

        scene.add(stageGroup);

        // ---------------------------------------------------------
        // 3D Foliar Leaf Specimen (Compound leaf with vein relief)
        // ---------------------------------------------------------
        const leafGroup = new THREE.Group();
        leafGroup.position.set(0, 0.12, 0);

        const leafLength = 1.9;
        const leafWidth = 0.95;
        const leafGeo = new THREE.PlaneGeometry(leafWidth, leafLength, 16, 24);
        const pos = leafGeo.attributes.position;

        for (let i = 0; i < pos.count; i++) {
            const y = pos.getY(i);
            const x = pos.getX(i);
            const normY = (y + leafLength / 2) / leafLength;

            // Natural pointed lanceolate/ovate leaf shape
            const widthScale = Math.sin(normY * Math.PI) * (1.1 - 0.3 * normY);
            pos.setX(i, x * widthScale);

            // Natural longitudinal curvature & central midrib depression
            const archZ = Math.sin(normY * Math.PI) * 0.12;
            const midribDip = -Math.abs(x / leafWidth) * 0.04;
            pos.setZ(i, archZ + midribDip);
        }
        leafGeo.computeVertexNormals();

        const leafBaseColor = new THREE.Color(0x3e7a3a);
        const leafMat = new THREE.MeshStandardMaterial({
            color: leafBaseColor,
            roughness: 0.65,
            metalness: 0.05,
            side: THREE.DoubleSide
        });
        const leafMesh = new THREE.Mesh(leafGeo, leafMat);
        leafMesh.rotation.x = -Math.PI / 2 + 0.15;
        leafMesh.castShadow = true;
        leafGroup.add(leafMesh);

        // Central Midrib Vein
        const midribGeo = new THREE.CylinderGeometry(0.015, 0.025, leafLength * 0.95, 8);
        midribGeo.rotateX(Math.PI / 2);
        const midribMat = new THREE.MeshStandardMaterial({ color: 0x5a944e, roughness: 0.6 });
        const midrib = new THREE.Mesh(midribGeo, midribMat);
        midrib.position.set(0, 0.02, 0);
        midrib.rotation.x = 0.15;
        leafGroup.add(midrib);

        // Secondary Vein pairs (lateral veins)
        for (let v = 0; v < 5; v++) {
            const vy = -0.5 + v * 0.25;
            const veinGeo = new THREE.CylinderGeometry(0.008, 0.01, 0.28, 6);
            const vLeft = new THREE.Mesh(veinGeo, midribMat);
            vLeft.position.set(-0.14, 0.015, vy);
            vLeft.rotation.set(0.15, 0, 0.65);
            leafGroup.add(vLeft);

            const vRight = new THREE.Mesh(veinGeo, midribMat);
            vRight.position.set(0.14, 0.015, vy);
            vRight.rotation.set(0.15, 0, -0.65);
            leafGroup.add(vRight);
        }

        // Dynamic Symptom Lesion Spot Meshes
        const lesionsGroup = new THREE.Group();
        leafGroup.add(lesionsGroup);

        scene.add(leafGroup);

        // Holographic Laser Scan Plane
        const scanLaserGeo = new THREE.PlaneGeometry(1.6, 0.08);
        const scanLaserMat = new THREE.MeshBasicMaterial({
            color: 0x48bb78,
            transparent: true,
            opacity: 0,
            side: THREE.DoubleSide
        });
        const scanLaser = new THREE.Mesh(scanLaserGeo, scanLaserMat);
        scanLaser.rotation.x = -Math.PI / 2 + 0.15;
        scene.add(scanLaser);

        // Pointer controls
        const controls = createPointerDragController(renderer.domElement, {
            initialAzimuth: 0.2,
            initialPolar: 0.75,
            minPolar: 0.35,
            maxPolar: 1.15,
            autoRotateSpeed: 0.002
        });

        let isRunning = false;
        let isScanning = false;
        let scanProgress = 0;

        function startScanEffect() {
            isScanning = true;
            scanProgress = 0;
            scanLaserMat.opacity = 0.85;
            // Clear prior lesions during active scan
            while (lesionsGroup.children.length > 0) {
                lesionsGroup.remove(lesionsGroup.children[0]);
            }
            leafMat.color.set(0x3e7a3a);
        }

        function endScanEffect(predictionData) {
            isScanning = false;
            scanLaserMat.opacity = 0;

            // Map morphological symptom patterns onto 3D specimen leaf
            while (lesionsGroup.children.length > 0) {
                lesionsGroup.remove(lesionsGroup.children[0]);
            }

            if (!predictionData) return;
            const pred = (predictionData.predicted_class || "").toLowerCase();

            if (pred.includes("healthy") || pred.includes("صحت مند")) {
                leafMat.color.set(0x388e3c); // Lush healthy green
            } else if (pred.includes("early_blight") || pred.includes("جھلساؤ")) {
                // Concentric brown rings with chlorotic yellow halo
                leafMat.color.set(0x566d3a);
                const spotGeo = new THREE.CircleGeometry(0.12, 12);
                spotGeo.rotateX(-Math.PI / 2 + 0.15);
                const spotMat = new THREE.MeshBasicMaterial({ color: 0x4a2a16, depthWrite: false });
                const haloGeo = new THREE.CircleGeometry(0.18, 12);
                haloGeo.rotateX(-Math.PI / 2 + 0.15);
                const haloMat = new THREE.MeshBasicMaterial({ color: 0xccb839, depthWrite: false });

                const coords = [[-0.12, -0.2], [0.15, 0.18], [-0.08, 0.42]];
                coords.forEach(([sx, sy]) => {
                    const halo = new THREE.Mesh(haloGeo, haloMat);
                    halo.position.set(sx, 0.03, sy);
                    lesionsGroup.add(halo);

                    const spot = new THREE.Mesh(spotGeo, spotMat);
                    spot.position.set(sx, 0.035, sy);
                    lesionsGroup.add(spot);
                });
            } else if (pred.includes("rust") || pred.includes("زنگ")) {
                // Cinnamon orange pustules
                leafMat.color.set(0x4f6838);
                const rustGeo = new THREE.SphereGeometry(0.045, 6, 6);
                const rustMat = new THREE.MeshStandardMaterial({ color: 0xbd5a17, roughness: 0.6 });
                for (let r = 0; r < 9; r++) {
                    const rust = new THREE.Mesh(rustGeo, rustMat);
                    rust.position.set((Math.random() - 0.5) * 0.45, 0.035, (Math.random() - 0.5) * 0.9);
                    lesionsGroup.add(rust);
                }
            } else {
                // General necrotic discoloration
                leafMat.color.set(0x4f5e3b);
                const necGeo = new THREE.CircleGeometry(0.08, 10);
                necGeo.rotateX(-Math.PI / 2 + 0.15);
                const necMat = new THREE.MeshBasicMaterial({ color: 0x3d281a });
                for (let n = 0; n < 4; n++) {
                    const nec = new THREE.Mesh(necGeo, necMat);
                    nec.position.set((Math.random() - 0.5) * 0.35, 0.035, (Math.random() - 0.5) * 0.7);
                    lesionsGroup.add(nec);
                }
            }
        }

        function animate() {
            if (!isRunning) return;
            requestAnimationFrame(animate);

            const { azimuth, polar } = controls.update(true);
            const radius = 3.6;
            camera.position.x = radius * Math.sin(polar) * Math.sin(azimuth);
            camera.position.z = radius * Math.sin(polar) * Math.cos(azimuth);
            camera.position.y = radius * Math.cos(polar);
            camera.lookAt(0, 0.25, 0);

            // Optical Laser Sweep
            if (isScanning) {
                scanProgress += 0.022;
                const sweepY = Math.sin(scanProgress * Math.PI) * 1.5 - 0.75;
                scanLaser.position.set(0, 0.16 + sweepY * 0.15, sweepY);
            }

            renderer.render(scene, camera);
        }

        function onResize() {
            if (!container) return;
            const w = container.clientWidth;
            const h = container.clientHeight || 320;
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
            renderer.setSize(w, h);
        }
        window.addEventListener("resize", onResize, { passive: true });

        return {
            start() {
                if (!isRunning) {
                    isRunning = true;
                    animate();
                }
            },
            pause() {
                isRunning = false;
            },
            triggerScan: startScanEffect,
            completeScan: endScanEffect,
            resize: onResize
        };
    }

    // -------------------------------------------------------------
    // Global Orchestration & Visibility Management
    // -------------------------------------------------------------
    function initCropCare3D() {
        state.webglAvailable = isWebGLSupported();

        if (!state.webglAvailable) {
            console.warn("CropCare AI: WebGL not available or supported. Displaying fallback static botanical graphics.");
            document.querySelectorAll(".fallback-botanical-graphic").forEach(el => {
                el.style.display = "block";
            });
            document.querySelectorAll(".three-canvas-wrapper").forEach(el => {
                el.style.display = "none";
            });
            return;
        }

        // Initialize 3D Scenes
        state.hero = initHeroWheatScene();
        state.field = initFieldScene();
        state.scanner = initScannerLeafScene();

        // Populate initial field crops if available globally
        if (window.currentCrops && state.field) {
            state.field.updateCrops(window.currentCrops);
        }

        // Tab Switching Listener: only run render loop for active tab
        function updateTabVisibility(tabId) {
            state.activeTab = tabId;
            if (state.hero) {
                if (tabId === "tab-dashboard") state.hero.start();
                else state.hero.pause();
            }
            if (state.field) {
                if (tabId === "tab-crops") {
                    state.field.start();
                    state.field.resize();
                } else state.field.pause();
            }
            if (state.scanner) {
                if (tabId === "tab-scanner") {
                    state.scanner.start();
                    state.scanner.resize();
                } else state.scanner.pause();
            }
        }

        // Listen for tab button clicks
        document.querySelectorAll(".nav-tab-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const targetTab = btn.getAttribute("data-tab");
                updateTabVisibility(targetTab);
            });
        });

        // IntersectionObserver: Pause when out of screen viewport to save 100% GPU
        if (window.IntersectionObserver) {
            const obs = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    const id = entry.target.id;
                    const isVisible = entry.isIntersecting;
                    if (id === "hero-3d-card" && state.hero) {
                        if (isVisible && state.activeTab === "tab-dashboard") state.hero.start();
                        else state.hero.pause();
                    }
                    if (id === "field-3d-card" && state.field) {
                        if (isVisible && state.activeTab === "tab-crops") state.field.start();
                        else state.field.pause();
                    }
                    if (id === "scanner-3d-card" && state.scanner) {
                        if (isVisible && state.activeTab === "tab-scanner") state.scanner.start();
                        else state.scanner.pause();
                    }
                });
            }, { threshold: 0.1 });

            const heroCard = document.getElementById("hero-3d-card");
            if (heroCard) obs.observe(heroCard);

            const fieldCard = document.getElementById("field-3d-card");
            if (fieldCard) obs.observe(fieldCard);

            const scannerCard = document.getElementById("scanner-3d-card");
            if (scannerCard) obs.observe(scannerCard);
        }

        // Expose public API on window for main.js coordination
        window.CropCare3D = {
            updateFieldCrops(crops) {
                if (state.field) state.field.updateCrops(crops);
            },
            triggerScannerStart() {
                if (state.scanner) state.scanner.triggerScan();
            },
            triggerScannerComplete(prediction) {
                if (state.scanner) state.scanner.completeScan(prediction);
            },
            setHeroWind(mode) {
                if (state.hero) state.hero.setWindVelocity(mode);
            },
            setHeroStage(stage) {
                if (state.hero) state.hero.applyGrowthStage(stage);
            }
        };
    }

    // Auto-initialize when DOM is ready
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initCropCare3D);
    } else {
        initCropCare3D();
    }
})();
