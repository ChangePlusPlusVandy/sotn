import { auth } from "@clerk/nextjs/server";

const FollowUpsPage = async () => {
  await auth.protect();

  return (
    <>
      <h1 className="text-2xl font-semibold">Follow-ups</h1>
      <p>TODO: Follow-up tasks grouped by Not started, In progress and Complete.</p>
    </>
  );
};

export default FollowUpsPage;
