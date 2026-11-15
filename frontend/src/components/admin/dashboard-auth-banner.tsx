"use client";

import { SignInButton } from "@clerk/nextjs";

import { Button } from "@/components/ui/button";

type DashboardAuthBannerProps = {
  mode: "live" | "preview" | "error";
  message?: string;
};

const DashboardAuthBanner = ({ mode, message }: DashboardAuthBannerProps) => {
  if (mode === "live") {
    return (
      <p className="border border-border bg-muted/40 px-3 py-2 text-sm">
        Showing live data from <code>GET /admin/stats</code>.
      </p>
    );
  }

  return (
    <div className="flex flex-wrap items-center justify-between gap-3 border border-border bg-muted/40 px-3 py-2 text-sm">
      <p>
        {mode === "error"
          ? (message ?? "Could not load live stats. Showing sample data.")
          : "Viewing without sign-in — sample data only. Sign in for live backend stats."}
      </p>
      <SignInButton mode="modal">
        <Button type="button" variant="outline" size="sm">
          Sign in for live data
        </Button>
      </SignInButton>
    </div>
  );
};

export default DashboardAuthBanner;
