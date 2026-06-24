"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

interface Party {
  id: string;
  name: string;
  created_at: string;
}

export default function HomePage() {
  const router = useRouter();
  const [parties, setParties] = useState<Party[]>([]);
  const [loading, setLoading] = useState(true);
  const [newName, setNewName] = useState("");
  const [error, setError] = useState("");
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/login");
      return;
    }
    fetch("/api/parties")
      .then((r) => r.json())
      .then((data: Party[]) => {
        setParties(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [router]);

  const handleCreate = async () => {
    const token = localStorage.getItem("access_token");
    if (!token) return;
    setCreating(true);
    setError("");
    try {
      const resp = await fetch("/api/parties", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newName || "My Party" }),
      });
      if (!resp.ok) throw new Error("Failed to create");
      const party: Party = await resp.json();
      router.push(`/party/${party.id}`);
    } catch {
      setError("Failed to create party");
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white flex flex-col items-center justify-center p-6">
      <h1 className="text-3xl font-bold mb-2">Agent Party</h1>
      <p className="text-slate-400 mb-8">Choose or create a party to join</p>

      {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

      {/* Quick create */}
      <div className="flex gap-2 mb-8 w-full max-w-md">
        <input
          type="text"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          placeholder="Party name (optional)"
          className="flex-1 px-3 py-2 rounded-lg bg-slate-800 border border-slate-600 text-white placeholder-slate-500 outline-none focus:border-violet-500 text-sm"
        />
        <button
          onClick={handleCreate}
          disabled={creating}
          className="px-4 py-2 rounded-lg bg-violet-600 hover:bg-violet-500 disabled:opacity-40 disabled:cursor-not-allowed text-white text-sm font-medium transition"
        >
          {creating ? "Creating…" : "New Party"}
        </button>
      </div>

      {/* Party list */}
      <div className="w-full max-w-md">
        <h2 className="text-sm font-semibold text-slate-300 mb-2 uppercase tracking-wider">
          Existing Parties
        </h2>
        {loading ? (
          <p className="text-slate-500 text-sm text-center py-4">Loading…</p>
        ) : parties.length === 0 ? (
          <p className="text-slate-500 text-sm text-center py-4">No parties yet — create one!</p>
        ) : (
          <div className="space-y-2">
            {parties.map((party) => (
              <button
                key={party.id}
                onClick={() => router.push(`/party/${party.id}`)}
                className="w-full text-left px-4 py-3 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 transition text-sm"
              >
                <div className="font-medium">{party.name}</div>
                <div className="text-xs text-slate-500 mt-0.5">{party.id}</div>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
