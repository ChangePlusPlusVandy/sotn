import { auth } from "@clerk/nextjs/server";

const ResourcesPage = async () => {
  await auth.protect();

  return (
    <>
      <h1 className="text-2xl font-semibold">Resources</h1>
      <p>TODO: Preview, add and edit the videos and PDFs shown to users.</p>
    </>
  );
};

export default ResourcesPage;
