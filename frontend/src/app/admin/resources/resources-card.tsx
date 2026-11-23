import { KIND_LABELS, ROLE_LABELS, type Resource } from "./mock-data";

type ResourceCardProps = {
  resource: Resource;
};

export const ResourceCard = ({ resource }: ResourceCardProps) => {
  return (
    <div className="flex flex-col gap-4 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
      {/* Top row: kind badge on the left, audience badges on the right */}
      <div className="flex items-start justify-between gap-2">
        <span className="rounded-full border border-gray-300 px-3 py-1 text-sm font-medium">
          {KIND_LABELS[resource.kind]}
        </span>

        <div className="flex flex-wrap justify-end gap-2">
          {resource.audiences.map((role) => (
            <span
              key={role}
              className="rounded-full border border-gray-300 px-3 py-1 text-sm font-medium"
            >
              {ROLE_LABELS[role]}
            </span>
          ))}
        </div>
      </div>

      {/* Title, plus a Draft label if not published */}
      <div className="flex items-center gap-2">
        <h2 className="text-lg font-medium">{resource.title}</h2>
        {!resource.is_published && (
          <span className="rounded-full bg-yellow-100 px-2 py-0.5 text-xs font-medium text-yellow-800">
            Draft
          </span>
        )}
      </div>

      {/* Buttons */}
      <div className="mt-auto grid grid-cols-2 gap-3">
        <button
          type="button"
          className="rounded-lg border border-gray-300 py-2 text-sm font-medium hover:bg-gray-50"
        >
          Edit
        </button>
        <a
          href={resource.url}
          target="_blank"
          rel="noopener noreferrer"
          className="rounded-lg border border-gray-300 py-2 text-center text-sm font-medium hover:bg-gray-50"
        >
          Preview
        </a>
      </div>
    </div>
  );
};