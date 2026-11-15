"use client";

import Link from "next/link";
import { SignInButton } from "@clerk/nextjs";

import { Button } from "@/components/ui/button";

/** Default Overview gate: keep Clerk sign-in, with an explicit skip for preview. */
const DashboardSignInGate = () => {
  return (
    <div className="mx-auto flex max-w-lg flex-col gap-4 border p-6">
      <h1 className="text-2xl font-semibold">Overview</h1>
      <p className="text-muted-foreground">
        Sign in with a staff account to load live intake stats from the backend.
      </p>
      <div className="flex flex-wrap gap-2">
        <SignInButton mode="modal">
          <Button type="button">Sign in</Button>
        </SignInButton>
        <Button type="button" variant="outline" asChild>
          <Link href="/admin?preview=1">Continue without signing in</Link>
        </Button>
      </div>
      <p className="text-sm text-muted-foreground">
        Skipping shows sample data only. Live numbers still require sign-in.
      </p>
    </div>
  );
};

export default DashboardSignInGate;
