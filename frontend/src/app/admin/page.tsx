import { auth } from "@clerk/nextjs/server";
import { getServerApi } from "@/lib/api-server";

const AdminDashboardPage = async () => {
  await auth.protect();
  const api = await getServerApi();
  const { data, error } = await api.GET("/admin/inquiries", {
    params: { query: { page_size: 1 } },
  });

  return (
    <>
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      {error ? (
        <p>Error loading inquiries</p>
      ) : (
        <p>Total inquiries: {data.total}</p>
      )}
    </>
  );
};

export default AdminDashboardPage;
