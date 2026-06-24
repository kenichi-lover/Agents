"use client";

import { useMemo } from "react";
import { Color } from "three";

/**
 * Room geometry: floor + 3 walls.
 * Floor: 12 × 12, Walls: height 5.
 * Open side faces +Z (entrance).
 */
export function RoomGeometry() {
  const floorMat = useMemo(() => new Color("#1e1e2e"), []);
  const wallMat = useMemo(() => new Color("#2a2a3c"), []);

  return (
    <group>
      {/* Floor */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
        <planeGeometry args={[12, 12]} />
        <meshStandardMaterial color={floorMat} roughness={0.8} metalness={0.1} />
      </mesh>

      {/* Back wall */}
      <mesh position={[0, 2.5, -6]} receiveShadow>
        <planeGeometry args={[12, 5]} />
        <meshStandardMaterial color={wallMat} roughness={0.9} />
      </mesh>

      {/* Left wall */}
      <mesh position={[-6, 2.5, 0]} rotation={[0, Math.PI / 2, 0]} receiveShadow>
        <planeGeometry args={[12, 5]} />
        <meshStandardMaterial color={wallMat} roughness={0.9} />
      </mesh>

      {/* Right wall */}
      <mesh position={[6, 2.5, 0]} rotation={[0, -Math.PI / 2, 0]} receiveShadow>
        <planeGeometry args={[12, 5]} />
        <meshStandardMaterial color={wallMat} roughness={0.9} />
      </mesh>

      {/* Ceiling (optional, subtle) */}
      <mesh rotation={[Math.PI / 2, 0, 0]} position={[0, 5, 0]}>
        <planeGeometry args={[12, 12]} />
        <meshStandardMaterial color="#151520" transparent opacity={0.6} />
      </mesh>
    </group>
  );
}
