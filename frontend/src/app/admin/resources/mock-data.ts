// Temporary fake data for building the Resources page.
// Matches ResourceRead in backend/app/schemas/resource.py.
// Delete once the page fetches from the real API.

export type ResourceKind = "pdf" | "video" | "link";
export type InquiryRole = "athlete" | "volunteer" | "partner" | "donor";

export type Resource = {
  id: string;
  title: string;
  description: string | null;
  kind: ResourceKind;
  url: string;
  audiences: InquiryRole[];
  is_published: boolean;
  created_at: string;
  updated_at: string;
};

// Display labels for the badges
export const KIND_LABELS: Record<ResourceKind, string> = {
  pdf: "PDF",
  video: "Video",
  link: "Link",
};

export const ROLE_LABELS: Record<InquiryRole, string> = {
  athlete: "Potential Athlete",
  volunteer: "Volunteer",
  partner: "Community Partner",
  donor: "Donor / Sponsor",
};

export const MOCK_RESOURCES: Resource[] = [
  {
    id: "1",
    title: "Welcome to SOTN",
    description: "A short intro video for new athletes and families.",
    kind: "video",
    url: "https://example.com/welcome",
    audiences: ["athlete"],
    is_published: true,
    created_at: "2026-10-01T12:00:00Z",
    updated_at: "2026-10-01T12:00:00Z",
  },
  {
    id: "2",
    title: "Athlete Medical & Release Form",
    description: null,
    kind: "pdf",
    url: "https://example.com/medical-form.pdf",
    audiences: ["athlete"],
    is_published: true,
    created_at: "2026-10-02T12:00:00Z",
    updated_at: "2026-10-02T12:00:00Z",
  },
  {
    id: "3",
    title: "Volunteering with SOTN",
    description: "What to expect as a new volunteer.",
    kind: "video",
    url: "https://example.com/volunteering",
    audiences: ["volunteer"],
    is_published: true,
    created_at: "2026-10-03T12:00:00Z",
    updated_at: "2026-10-03T12:00:00Z",
  },
  {
    id: "4",
    title: "Background Check Overview",
    description: null,
    kind: "pdf",
    url: "https://example.com/background-check.pdf",
    audiences: ["volunteer"],
    is_published: false, // a draft, to test how unpublished items look
    created_at: "2026-10-04T12:00:00Z",
    updated_at: "2026-10-04T12:00:00Z",
  },
  {
    id: "5",
    title: "Community Partner Toolkit",
    description: "Ways local organizations can get involved.",
    kind: "link",
    url: "https://example.com/partners",
    audiences: ["partner", "donor"], // multiple audiences, to test several badges
    is_published: true,
    created_at: "2026-10-05T12:00:00Z",
    updated_at: "2026-10-05T12:00:00Z",
  },
  {
    id: "6",
    title: "Sponsor Impact Report 2025",
    description: null,
    kind: "pdf",
    url: "https://example.com/impact-2025.pdf",
    audiences: ["donor"],
    is_published: true,
    created_at: "2026-10-06T12:00:00Z",
    updated_at: "2026-10-06T12:00:00Z",
  },
];