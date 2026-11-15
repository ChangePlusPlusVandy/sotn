import { auth } from "@clerk/nextjs/server";
import { connection } from "next/server";

import BreakdownList from "@/components/admin/breakdown-list";
import DashboardAuthBanner from "@/components/admin/dashboard-auth-banner";
import DashboardSignInGate from "@/components/admin/dashboard-sign-in-gate";
import IntakesOverTime from "@/components/admin/intakes-over-time";
import StatCard from "@/components/admin/stat-card";
import {
  SAMPLE_ADMIN_STATS,
  fetchAdminStats,
  type AdminStats,
} from "@/lib/admin-stats";

const formatLabel = (value: string | null) => {
  if (!value) return "Unspecified";
  return value.replaceAll("_", " ");
};

type AdminDashboardPageProps = {
  searchParams: Promise<{ preview?: string }>;
};

const DashboardBody = ({
  stats,
  mode,
  message,
}: {
  stats: AdminStats;
  mode: "live" | "preview" | "error";
  message?: string;
}) => {
  return (
    <div className="space-y-8">
      <DashboardAuthBanner mode={mode} message={message} />

      <header>
        <h1 className="text-2xl font-semibold">Overview</h1>
        <p className="text-muted-foreground">
          Snapshot of intake activity across Special Olympics Tennessee.
        </p>
      </header>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        <StatCard label="New intakes" value={stats.new_today} hint="Submitted today" />
        <StatCard
          label="Awaiting state review"
          value={stats.awaiting_contact}
          hint="Not contacted yet"
        />
        <StatCard
          label="Total in range"
          value={stats.total}
          hint="Default: last 30 days"
        />
      </section>

      <IntakesOverTime days={stats.by_day} />

      <section className="grid gap-4 lg:grid-cols-3">
        <BreakdownList
          title="User groups"
          items={stats.by_role.map(({ role, count }) => ({
            label: formatLabel(role),
            count,
          }))}
        />
        <BreakdownList
          title="Intakes by region"
          items={stats.by_region.map(({ region, count }) => ({
            label: formatLabel(region),
            count,
          }))}
        />
        <BreakdownList
          title="By status"
          items={stats.by_status.map(({ status, count }) => ({
            label: formatLabel(status),
            count,
          }))}
        />
      </section>
    </div>
  );
};

const AdminDashboardPage = async ({ searchParams }: AdminDashboardPageProps) => {
  await connection();
  const { isAuthenticated, getToken } = await auth();
  const { preview } = await searchParams;
  const wantsPreview = preview === "1";

  // Keep sign-in as the default path; only skip when they click through explicitly.
  if (!isAuthenticated && !wantsPreview) {
    return <DashboardSignInGate />;
  }

  if (!isAuthenticated && wantsPreview) {
    return <DashboardBody stats={SAMPLE_ADMIN_STATS} mode="preview" />;
  }

  try {
    const stats = await fetchAdminStats(getToken);
    return <DashboardBody stats={stats} mode="live" />;
  } catch (error) {
    const message =
      error instanceof Error
        ? `${error.message} Showing sample data instead.`
        : "Could not load live stats. Showing sample data.";
    return (
      <DashboardBody
        stats={SAMPLE_ADMIN_STATS}
        mode="error"
        message={message}
      />
    );
  }
};

export default AdminDashboardPage;
