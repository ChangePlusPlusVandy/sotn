import type { components } from "@/lib/api-types";

export type InquiryRole = components["schemas"]["InquiryRole"];
export type Program = components["schemas"]["ProgramPublic"];

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

// Must match the InquiryRole enum in the backend (see api-types.ts).
const ROLES: readonly InquiryRole[] = ["athlete", "volunteer", "partner", "donor"];

// Turns a value from the URL into a role, or undefined if it isn't one.
export const parseRole = (value: string | string[] | undefined): InquiryRole | undefined =>
  ROLES.find((role) => role === value);

// Active programs for one role, from the public GET /programs endpoint.
// Returns null when the backend can't be reached or answers with an error, so a page
// can show a message instead of crashing. An empty array means "no matching programs".
// TODO: switch to the typed API client once it is merged (PR #47).
export const getPrograms = async (role: InquiryRole): Promise<Program[] | null> => {
  try {
    const res = await fetch(`${API_URL}/programs?role=${role}`);
    if (!res.ok) {
      console.error(`GET /programs?role=${role} failed with status ${res.status}`);
      return null;
    }
    return (await res.json()) as Program[];
  } catch (error) {
    console.error("GET /programs failed", error);
    return null;
  }
};
