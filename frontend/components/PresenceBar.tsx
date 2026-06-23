"use client";

interface PresenceBarProps {
  isConnected: boolean;
  partyId: string;
}

export function PresenceBar({ isConnected, partyId }: PresenceBarProps) {
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
        <span className="hidden sm:inline">2 agents · 1 human</span>
        <span className="sm:hidden">3 online</span>
      </div>
    </div>
  );
}
