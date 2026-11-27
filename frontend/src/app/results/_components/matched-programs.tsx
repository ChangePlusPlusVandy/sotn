import Link from "next/link";
import { Button } from "@/components/ui/button";
import { getPrograms, parseRole } from "@/lib/programs";
import { CONTENT, LINKS } from "../content";
import { Panel } from "./panel";

// Programs for the visitor's role, which comes from the URL (/results?role=athlete).
// It reads searchParams and calls the backend, which both happen at request time, so the
// page renders this inside <Suspense> and the rest of the page can load without waiting.
export const MatchedPrograms = async ({
  searchParams,
}: {
  searchParams: PageProps<"/results">["searchParams"];
}) => {
  const role = parseRole((await searchParams).role);
  // Without a known role there is nothing to match, so show no card.
  if (!role) return null;

  const programs = await getPrograms(role);

  if (programs === null) {
    return (
      <Panel label={CONTENT.programs.label}>
        <p className="pt-1 text-sm text-ink-muted">{CONTENT.programs.loadError}</p>
      </Panel>
    );
  }
  if (programs.length === 0) return null;

  return (
    <Panel label={CONTENT.programs.label}>
      <p className="pt-1 text-sm text-ink-muted">{CONTENT.programs.intro}</p>
      <ul className="flex flex-col gap-2 pt-4">
        {programs.map((program) => (
          <li
            key={program.id}
            className="flex items-center justify-between gap-3 rounded-lg border border-line bg-white p-2.5"
          >
            <div className="min-w-0">
              <p className="text-sm font-medium text-ink">{program.name}</p>
              {program.description && (
                <p className="line-clamp-1 text-[11px] leading-[16.5px] text-ink-muted">
                  {program.description}
                </p>
              )}
            </div>
            <Button
              asChild
              variant="outline"
              className="h-8 rounded-md border-line px-3 text-xs text-ink"
            >
              <Link href={LINKS.startProgram}>{CONTENT.programs.start}</Link>
            </Button>
          </li>
        ))}
      </ul>
    </Panel>
  );
};

// Shown while the programs are loading.
export const MatchedProgramsSkeleton = () => {
  return (
    <Panel label={CONTENT.programs.label}>
      <div className="flex animate-pulse flex-col gap-2 pt-4" aria-hidden>
        <div className="h-[54px] rounded-lg bg-muted" />
        <div className="h-[54px] rounded-lg bg-muted" />
      </div>
    </Panel>
  );
};
