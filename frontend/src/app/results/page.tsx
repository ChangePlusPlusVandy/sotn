import { Suspense } from "react";
import Image from "next/image";
import Link from "next/link";
import { SiteHeader } from "@/components/site-header";
import { Button } from "@/components/ui/button";
import { CONTENT, LINKS } from "./content";
import { MatchedPrograms, MatchedProgramsSkeleton } from "./_components/matched-programs";
import { Panel } from "./_components/panel";

// Shown after the intake form is submitted. The visitor's role is passed in the URL,
// for example /results?role=athlete, and decides which programs are suggested.
const ResultsPage = ({ searchParams }: PageProps<"/results">) => {
  return (
    <>
      <SiteHeader />
      <main className="mx-auto w-full max-w-[672px] px-6 py-10">
        <div className="flex flex-col items-center text-center">
          <span className="flex size-14 items-center justify-center rounded-full bg-brand">
            <Image src="/results/check-white.svg" alt="" width={28} height={28} />
          </span>
          <h1 className="pt-6 text-[30px] leading-9 font-bold tracking-[-0.75px] text-ink">
            {CONTENT.heading}
          </h1>
          <p className="pt-2 text-base text-ink-muted">{CONTENT.subheading}</p>
        </div>

        <div className="mt-8 flex flex-col gap-4">
          <Suspense fallback={<MatchedProgramsSkeleton />}>
            <MatchedPrograms searchParams={searchParams} />
          </Suspense>

          <Panel label={CONTENT.nextSteps.label}>
            <ol className="flex flex-col gap-3 pt-3">
              {CONTENT.nextSteps.steps.map((step, index) => (
                <li key={step} className="flex items-center gap-3 text-sm text-ink">
                  <span className="flex size-6 shrink-0 items-center justify-center rounded-full bg-white text-xs font-medium">
                    {index + 1}
                  </span>
                  {step}
                </li>
              ))}
            </ol>
          </Panel>
        </div>

        <div className="flex justify-center pt-6">
          <Button asChild className="h-10 gap-2 bg-brand px-6 text-white hover:bg-brand/90">
            <Link href={LINKS.portal}>
              {CONTENT.portal}
              <Image src="/results/arrow-right-white.svg" alt="" width={16} height={16} />
            </Link>
          </Button>
        </div>
      </main>
    </>
  );
};

export default ResultsPage;
