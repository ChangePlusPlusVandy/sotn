import { auth } from "@clerk/nextjs/server";
import { TriageList } from "@/components/triage/triage-list";
import { SAMPLE_INQUIRIES } from "@/lib/sample-inquiries";

// Uses sample data until the page is wired to GET /admin/inquiries.
const TriagePage = async () => {
  await auth.protect();

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-2">
        <h1 className="text-4xl font-bold tracking-[-0.02em]">Intake triage</h1>
        <p className="text-sm text-sotn-grey-dark">Review, route, and follow up on submitted intakes.</p>
      </div>
      <TriageList inquiries={SAMPLE_INQUIRIES} />
    </div>
  );
};

export default TriagePage;
