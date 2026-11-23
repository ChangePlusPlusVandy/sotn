"use client";

import { useState } from "react";
import {
  KIND_LABELS,
  MOCK_PORTAL_RESOURCES,
  PROGRAMS,
  type PortalResourceKind,
  type Program,
} from "./mock-data";

const KINDS = Object.keys(KIND_LABELS) as PortalResourceKind[];

type ChipProps = {
  label: string;
  active: boolean;
  onClick: () => void;
};

const Chip = ({ label, active, onClick }: ChipProps) => (
  <button
    type="button"
    onClick={onClick}
    aria-pressed={active}
    className={`rounded-full border px-3 py-1 text-xs font-medium ${
      active
        ? "border-black bg-black text-white"
        : "border-gray-300 bg-white text-gray-800 hover:bg-gray-50"
    }`}
  >
    {label}
  </button>
);

export const ResourceBrowser = () => {
  const [query, setQuery] = useState("");
  const [program, setProgram] = useState<Program | "all">("all");
  const [kind, setKind] = useState<PortalResourceKind | "all">("all");

  const search = query.trim().toLowerCase();
  const filtered = MOCK_PORTAL_RESOURCES.filter(
    (r) =>
      (program === "all" || r.program === program) &&
      (kind === "all" || r.kind === kind) &&
      r.title.toLowerCase().includes(search),
  );

  return (
    <div className="flex flex-col gap-5">
      {/* Search */}
      <label className="flex flex-col gap-1 text-xs font-medium text-gray-700">
        Search
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search resources..."
          className="rounded-md border border-gray-300 px-3 py-2 text-sm font-normal"
        />
      </label>

      {/* Program filter */}
      <div className="flex flex-wrap gap-2">
        <Chip label="All programs" active={program === "all"} onClick={() => setProgram("all")} />
        {PROGRAMS.map((p) => (
          <Chip key={p} label={p} active={program === p} onClick={() => setProgram(p)} />
        ))}
      </div>

      {/* Type filter */}
      <div className="flex flex-wrap gap-2">
        <Chip label="All types" active={kind === "all"} onClick={() => setKind("all")} />
        {KINDS.map((k) => (
          <Chip key={k} label={KIND_LABELS[k]} active={kind === k} onClick={() => setKind(k)} />
        ))}
      </div>

      {/* Cards */}
      {filtered.length === 0 ? (
        <p className="text-sm text-gray-600">No resources match your filters.</p>
      ) : (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filtered.map((r) => (
            // TODO: link to /portal/resources/[id] once the detail page exists
            <a
              key={r.id}
              href={r.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex flex-col gap-3 rounded-lg border border-gray-200 bg-white p-4 hover:shadow-sm"
            >
              <div className="flex items-start justify-between">
                <span
                  aria-hidden="true"
                  className="flex h-7 w-7 items-center justify-center rounded-md bg-[#ECE8DC] text-sm"
                >
                  ↓
                </span>
                <span className="rounded-full bg-[#ECE8DC] px-2.5 py-0.5 text-xs font-medium">
                  {KIND_LABELS[r.kind]}
                </span>
              </div>
              <div>
                <h2 className="text-sm font-semibold">{r.title}</h2>
                <p className="text-xs text-gray-500">{r.subtitle}</p>
              </div>
            </a>
          ))}
        </div>
      )}
    </div>
  );
};