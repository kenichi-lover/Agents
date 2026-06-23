"use client";

interface RoundTableProps {
  partyId: string;
}

export function RoundTable({ partyId }: RoundTableProps) {
  return (
    <div className="flex flex-col h-full">
      <h3 className="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wider">
        Round Table
      </h3>
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <div className="text-3xl mb-2">🍽️</div>
          <p className="text-sm text-slate-500">Coming soon</p>
          <p className="text-xs text-slate-600 mt-1">
            Group conversations & threads
          </p>
        </div>
      </div>
    </div>
  );
}
