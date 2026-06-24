"use client";

import { useEffect, useState } from "react";

interface PresenceData {
  party_id: string;
  online_users: number;
  online_agents: number;
}

interface PresenceBarProps {
  isConnected: boolean;
  partyId: string;
}

export function PresenceBar({ isConnected, partyId }: PresenceBarProps) {
  const [presence, setPresence] = useState<PresenceData | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (!isConnected) return;
    const fetchPresence = async () => {
      try {
        const resp = await fetch(`/api/presence/${partyId}`);
        if (resp.ok) {
          const data = await resp.json();
          setPresence(data);
          setError(false);
        }
      } catch {
        setError(true);
      }
    };
    fetchPresence();
    const interval = setInterval(fetchPresence, 5000);
    return () => clearInterval(interval);
  }, [isConnected, partyId]);

  const totalOnline = presence
    ? presence.online_users + presence.online_agents
    : error
      ? "?"
      : "...";

  return (
    <div className="flex items-center justify-between px-4 py-2 bg-slate-800 border-b border-slate-700">
      <div className="flex items-center gap-3">
        <span className="text-sm font-medium text-slate-300">
          Party #{partyId.slice(0, 8)}
        </span>
        <span className="text-xs text-slate-500">|</span>
        <div className="flex items-center gap-1.5">
          <span
            className={`w-2 h-2 rounded-full ${
              isConnected ? "bg-emerald-400" : "bg-red-400"
            }`}
          />
          <span className="text-xs text-slate-400">
            {isConnected ? "Connected" : "Disconnected"}
          </span>
        </div>
      </div>
      <div className="flex items-center gap-2 text-xs text-slate-400">
        {presence ? (
          <>
            <span>{presence.online_users} user{presence.online_users !== 1 ? "s" : ""}</span>
            <span>·</span>
            <span>{presence.online_agents} agent{presence.online_agents !== 1 ? "s" : ""}</span>
          </>
        ) : (
          <span>{totalOnline} online</span>
        )}
      </div>
    </div>
  );
}
