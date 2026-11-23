export type PortalResourceKind = "pdf" | "video" | "guide" | "link";

export const KIND_LABELS: Record<PortalResourceKind, string> = {
  pdf: "PDF",
  video: "Video",
  guide: "Guide",
  link: "Link",
};

export const PROGRAMS = [
  "Sports",
  "Health",
  "Train 4 Life",
  "Inclusive Health",
  "UCS",
  "Athlete Leadership",
  "Volunteer",
  "Coaching",
  "Sponsors",
  "Give",
  "Vendors",
] as const;

export type Program = (typeof PROGRAMS)[number];

export type PortalResource = {
  id: number;
  title: string;
  kind: PortalResourceKind;
  program: Program;
  subtitle: string;
  url: string;
};

// TODO: replace with a real API call once the backend supports it
export const MOCK_PORTAL_RESOURCES: PortalResource[] = [
  { id: 1, title: "Welcome to SOTN", kind: "video", program: "Sports", subtitle: "Sports Programming", url: "#" },
  { id: 2, title: "Athlete Medical & Release Form", kind: "pdf", program: "Sports", subtitle: "Sports Programming", url: "#" },
  { id: 3, title: "First-Season Family Guide", kind: "guide", program: "Sports", subtitle: "Sports Programming", url: "#" },
  { id: 4, title: "Healthy Athletes Screening Calendar", kind: "link", program: "Health", subtitle: "Health Screenings", url: "#" },
  { id: 5, title: "Clinical Volunteer Handbook", kind: "pdf", program: "Health", subtitle: "Health Screenings", url: "#" },
  { id: 6, title: "Train 4 Life Starter Plan", kind: "guide", program: "Train 4 Life", subtitle: "Train 4 Life", url: "#" },
  { id: 7, title: "UCS Playbook", kind: "pdf", program: "UCS", subtitle: "Unified Champion Schools", url: "#" },
  { id: 8, title: "Volunteering with SOTN", kind: "video", program: "Volunteer", subtitle: "Volunteer", url: "#" },
  { id: 9, title: "Coach Certification Pathway", kind: "guide", program: "Coaching", subtitle: "Coaching", url: "#" },
];