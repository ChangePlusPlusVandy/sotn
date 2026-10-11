import { auth } from "@clerk/nextjs/server";

const AdminDashboardPage = async () => {
  await auth.protect();

  return (
    <>
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      <p>TODO: Intake counts, intakes over time, and breakdowns by region, referral source and user group.</p>
    </>
  );
};

export default AdminDashboardPage;
