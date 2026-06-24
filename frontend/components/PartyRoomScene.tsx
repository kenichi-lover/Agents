"use client";

import { memo, Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { RoomGeometry } from "./RoomGeometry";
import { RoundTable3D } from "./RoundTable3D";
import { AgentAvatars } from "./AgentAvatars";

/* ------------------------------------------------------------------ */
/*  Lighting                                                           */
/* ------------------------------------------------------------------ */

function Lighting() {
  return (
    <>
      {/* Ambient base */}
      <ambientLight intensity={0.4} color="#c4b5fd" />

      {/* Warm overhead */}
      <directionalLight position={[0, 8, 0]} intensity={0.3} castShadow color="#fef3c7" />

      {/* Point lights near table corners */}
      <pointLight position={[-4, 4, -4]} intensity={0.6} color="#fde68a" distance={12} />
      <pointLight position={[4, 4, -4]} intensity={0.6} color="#fde68a" distance={12} />

      {/* Subtle fill */}
      <pointLight position={[0, 3, 4]} intensity={0.3} color="#a5b4fc" distance={10} />
    </>
  );
}

/* ------------------------------------------------------------------ */
/*  Canvas wrapper (lazy-loaded to avoid SSR issues)                   */
/* ------------------------------------------------------------------ */

const PartyRoomCanvas = memo(function PartyRoomCanvas() {
  return (
    <Canvas
      shadows
      camera={{ position: [0, 8, 10], fov: 50, near: 0.1, far: 100 }}
      gl={{ antialias: true, alpha: false }}
    >
      {/* Background matching dark theme */}
      <color attach="background" args={["#0f0a1a"]} />

      <Lighting />

      <Suspense fallback={null}>
        <RoomGeometry />
        <RoundTable3D />
        <AgentAvatars />
      </Suspense>

      {/* Orbit controls — rotate/zoom the room */}
      <OrbitControls
        makeDefault
        minPolarAngle={0.2}
        maxPolarAngle={Math.PI / 2.2}
        minDistance={5}
        maxDistance={20}
        target={[0, 0.5, 0]}
      />
    </Canvas>
  );
});

/* ------------------------------------------------------------------ */
/*  Export                                                             */
/* ------------------------------------------------------------------ */

export { PartyRoomCanvas };
