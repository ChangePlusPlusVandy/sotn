"use client";

import { Button } from "@/components/ui/button";

// Catches errors thrown by admin pages, e.g. the backend being unreachable.
// Error responses from the API come back as `{ error }` and are handled in each page.
const AdminError = ({ retry }: { error: Error & { digest?: string }; retry: () => void }) => {
  return (
    <>
      <h1 className="text-2xl font-semibold">Something went wrong</h1>
      <p>Couldn&apos;t load this page. The server may be unavailable.</p>
      <Button variant="outline" onClick={() => retry()}>
        Try again
      </Button>
    </>
  );
};

export default AdminError;
