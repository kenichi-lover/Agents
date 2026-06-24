"use client";

import { usePartyStore } from "@/stores/partyStore";

interface RoundTableProps {
  partyId: string;
}

/**
 * RoundTable sidebar — toggles between round-table mode and scatter mode.
 * When in round-table mode, agents arrange around the 3D table.
 */
export function RoundTable({ partyId }: RoundTableProps) {
  const roundTableMode = usePartyStore((s) => s.roundTableMode);
  const arrangeRoundTable = usePartyStore((s) => s.arrangeRoundTable);
  const scatterAgents = usePartyStore((s) => s.scatterAgents);

  const handleToggle = () => {
    if (!roundTableMode) {
      arrangeRoundTable(2.5, 0, 0); // radius 2.5, centered at origin
    } else {
      scatterAgents(partyId, 8);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">
          Round Table
        </h3>
        <button
          onClick={handleToggle}
          className={`px-2 py-1 text-xs rounded-full transition ${
            roundTableMode
              ? "bg-violet-600 text-white hover:bg-violet-500"
              : "bg-slate-700 text-slate-300 hover:bg-slate-600"
          }`}
        >
          {roundTableMode ? "Active" : "Activate"}
        </button>
      </div>

      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <div className="text-3xl mb-2">🍽️</div>
          <p className="text-xs text-slate-500">
            {roundTableMode
              ? "Agents gathered around the table"
              : "Click Activate to start a round table discussion"}
          </p>
        </div>
      </div>
    </div>
  );
}
