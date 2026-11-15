import type { components } from "@/lib/api-types";

export type Inquiry = components["schemas"]["InquiryRead"];
export type InquiryStatus = components["schemas"]["InquiryStatus"];
export type InquiryRole = components["schemas"]["InquiryRole"];

export const STATUS_LABELS: Record<InquiryStatus, string> = {
  new: "New",
  needs_review: "Needs review",
  assigned: "Assigned",
  contacted: "Contacted",
  referred: "Referred",
  closed: "Closed",
};

export const ROLE_LABELS: Record<InquiryRole, string> = {
  athlete: "Athlete",
  volunteer: "Volunteer",
  partner: "Partner",
  donor: "Donor",
};
