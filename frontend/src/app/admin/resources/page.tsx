import { auth } from "@clerk/nextjs/server";
import { MOCK_RESOURCES } from "./mock-data";
import { ResourceCard } from "./resources-card";

const ResourcesPage = async () => {
  await auth.protect();

  // TODO: replace with a real API call to GET /resources
  const resources = MOCK_RESOURCES;

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Resources</h1>
          <p className="text-gray-600">Materials sent to users after routing.</p>
        </div>
        <button
          type="button"
          className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium shadow-sm hover:bg-gray-50"
        >
          + Add resource
        </button>
      </div>

      {/* Grid of cards: 1 column on phones, 2 on tablets, 3 on desktop */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {resources.map((resource) => (
          <ResourceCard key={resource.id} resource={resource} />
        ))}
      </div>
    </div>
  );
};

export default ResourcesPage;