import type { ReactNode } from "react";

// The white rounded card with a small uppercase label used on the results page.
export const Panel = ({ label, children }: { label: string; children: ReactNode }) => {
  return (
    <section className="rounded-2xl border border-line bg-white p-6">
      <h2 className="text-xs leading-4 font-medium tracking-[0.6px] text-ink-muted uppercase">
        {label}
      </h2>
      {children}
    </section>
  );
};
