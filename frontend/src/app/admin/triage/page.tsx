import { auth } from "@clerk/nextjs/server";

const TriagePage = async () => {
  await auth.protect();

  return (
    <>
      <h1 className="text-2xl font-semibold">Intake triage</h1>
      <p>TODO: All submissions with search and filters (GET /admin/intakes); open one to review, route and add notes.</p>
    </>
  );
};

export default TriagePage;
