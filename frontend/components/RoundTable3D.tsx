"use client";

import { useMemo } from "react";
import { Color } from "three";

/**
 * 3D round table at the center of the room.
 * Cylinder top + 3 legs.
 */
export function RoundTable3D() {
  const topColor = useMemo(() => "#5c3d2e", []);
  const legColor = useMemo(() => "#3e2723", []);

  return (
    <group position={[0, 0, 0]}>
      {/* Table top */}
      <mesh position={[0, 0.75, 0]} castShadow receiveShadow>
        <cylinderGeometry args={[1.5, 1.5, 0.1, 32]} />
        <meshStandardMaterial color={topColor} roughness={0.6} metalness={0.1} />
      </mesh>

      {/* Table rim (thin torus) */}
      <mesh position={[0, 0.8, 0]} rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[1.5, 0.03, 8, 32]} />
        <meshStandardMaterial color={legColor} roughness={0.4} metalness={0.2} />
      </mesh>

      {/* 3 legs */}
      {[0, 1, 2].map((i) => {
        const angle = (2 * Math.PI * i) / 3;
        const legX = 0.8 * Math.cos(angle);
        const legZ = 0.8 * Math.sin(angle);
        return (
          <mesh key={i} position={[legX, 0.35, legZ]} castShadow>
            <cylinderGeometry args={[0.04, 0.05, 0.7, 8]} />
            <meshStandardMaterial color={legColor} roughness={0.7} />
          </mesh>
        );
      })}
    </group>
  );
}
