"use client";

import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import { Html } from "@react-three/drei";
import { Vector3, Mesh } from "three";

declare global {
  namespace JSX {
    interface IntrinsicElements {
      [name: string]: any;
    }
  }
}

interface AgentAvatarProps {
  id: string;
  name: string;
  color: string;
  position: [number, number, number];
  targetPosition: [number, number, number];
  isUser?: boolean;
}

/**
 * Single agent avatar: capsule body + name label.
 * Smoothly lerps position each frame.
 * Gentle idle bob animation.
 */
export function AgentAvatar({
  id,
  name,
  color,
  position,
  targetPosition,
  isUser = false,
}: AgentAvatarProps) {
  const meshRef = useRef<Mesh>(null);
  const target = useRef(new Vector3(...targetPosition));
  const pos = useRef(new Vector3(...position));

  // Smooth lerp
  useFrame((_state, delta) => {
    if (!meshRef.current) return;
    target.current.set(...targetPosition);
    pos.current.lerp(target.current, Math.min(delta * 3, 1));
    meshRef.current.position.copy(pos.current);

    // Idle bob
    meshRef.current.position.y = 0.6 + Math.sin(Date.now() * 0.002 + parseFloat(id) * 100) * 0.05;
  });

  const emissiveColor = useMemo(() => color, [color]);

  return (
    <group>
      {/* Capsule body */}
      <mesh ref={meshRef} castShadow position={[0, 0.6, 0]}>
        <capsuleGeometry args={[0.2, 0.8, 8, 16]} />
        <meshStandardMaterial
          color={color}
          emissive={emissiveColor}
          emissiveIntensity={0.3}
          roughness={0.5}
          metalness={0.2}
        />
      </mesh>

      {/* User ring */}
      {isUser && (
        <mesh position={[0, 0.05, 0]} rotation={[Math.PI / 2, 0, 0]}>
          <torusGeometry args={[0.3, 0.02, 8, 24]} />
          <meshStandardMaterial color="#ffffff" emissive="#ffffff" emissiveIntensity={0.5} />
        </mesh>
      )}

      {/* Name label */}
      <Html
        position={[0, 1.4, 0]}
        center
        distanceFactor={15}
        style={{
          pointerEvents: "none",
          textAlign: "center",
          transform: "translate(-50%, -100%)",
        }}
      >
        <div
          className="text-xs font-medium whitespace-nowrap px-2 py-0.5 rounded-full backdrop-blur-sm"
          style={{
            backgroundColor: `${color}cc`,
            color: "#fff",
            textShadow: "0 1px 2px rgba(0,0,0,0.5)",
          }}
        >
          {name}
        </div>
      </Html>
    </group>
  );
}
