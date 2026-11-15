/**
 * Types + fetch for GET /admin/stats.
 * Kept separate from generated api-types.ts until that file is regenerated after the stats API merges.
 */

const baseUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type DayCount = { date: string; count: number };
export type RoleCount = { role: string; count: number };
export type RegionCount = { region: string | null; count: number };
export type StatusCount = { status: string; count: number };

export type AdminStats = {
  new_today: number;
  awaiting_contact: number;
  total: number;
  by_day: DayCount[];
  by_role: RoleCount[];
  by_region: RegionCount[];
  by_status: StatusCount[];
};

export type AdminStatsQuery = {
  start?: string;
  end?: string;
};

/** Sample payload so Overview can render without a staff session. */
export const SAMPLE_ADMIN_STATS: AdminStats = {
  new_today: 7,
  awaiting_contact: 23,
  total: 212,
  by_day: [
    { date: "2026-10-01", count: 6 },
    { date: "2026-10-02", count: 9 },
    { date: "2026-10-03", count: 4 },
    { date: "2026-10-04", count: 12 },
    { date: "2026-10-05", count: 8 },
  ],
  by_role: [
    { role: "athlete", count: 80 },
    { role: "volunteer", count: 44 },
    { role: "partner", count: 28 },
    { role: "donor", count: 20 },
  ],
  by_region: [
    { region: "east", count: 61 },
    { region: "middle", count: 68 },
    { region: "west", count: 48 },
    { region: null, count: 35 },
  ],
  by_status: [
    { status: "new", count: 15 },
    { status: "needs_review", count: 8 },
    { status: "assigned", count: 6 },
    { status: "contacted", count: 12 },
  ],
};

export async function fetchAdminStats(
  getToken: () => Promise<string | null>,
  query: AdminStatsQuery = {},
): Promise<AdminStats> {
  const url = new URL("/admin/stats", baseUrl);
  if (query.start) url.searchParams.set("start", query.start);
  if (query.end) url.searchParams.set("end", query.end);

  const token = await getToken();
  const res = await fetch(url, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Failed to load admin stats (${res.status})`);
  }

  return res.json() as Promise<AdminStats>;
}
