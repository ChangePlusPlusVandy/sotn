import { auth } from "@clerk/nextjs/server";
import { ResourceBrowser } from "./resource-browser";

const PortalResourcesPage = async () => {
  await auth.protect();

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-3xl font-bold">Resources</h1>
        <p className="text-sm text-gray-600">
          Forms, guides, and videos for every program.
        </p>
      </div>
      <ResourceBrowser />
    </div>
  );
};

export default PortalResourcesPage;