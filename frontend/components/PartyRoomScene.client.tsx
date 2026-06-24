"use client";

import dynamic from "next/dynamic";
import { Suspense } from "react";

const PartyRoomCanvas = dynamic(() => import("./PartyRoomScene").then((m) => m.PartyRoomCanvas), {
  ssr: false,
  loading: () => (
    <div className="absolute inset-0 bg-[#0f0a1a] flex items-center justify-center">
      <span className="text-slate-500 text-sm">Loading 3D scene…</span>
    </div>
  ),
});

interface PartyRoomSceneProps {
  partyId: string;
}

/**
 * PartyRoomScene — wraps the 3D canvas with suspense fallback.
 * The canvas is client-only (ssr: false).
 */
export function PartyRoomScene({ partyId }: PartyRoomSceneProps) {
  return (
    <Suspense
      fallback={
        <div className="absolute inset-0 bg-[#0f0a1a] flex items-center justify-center">
          <span className="text-slate-500 text-sm">Loading 3D scene…</span>
        </div>
      }
    >
      <PartyRoomCanvas />
    </Suspense>
  );
}
