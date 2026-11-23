import { components } from "@/lib/api-types";
import { ReactNode } from "react";

export type InquiryRole = components["schemas"]["InquiryRole"];
type InquiryCreate = components["schemas"]["InquiryCreate"];

export type Option<T extends string = string> = { value: T; label: string };
type ValueOf<T extends readonly Option[]> = T[number]["value"];

// Step 1
export const WHO_FOR_OPTIONS = [
  { value: "me", label: "It's me" },
  { value: "someone_else", label: "Someone else" },
] as const;

// Step 2
export const ROLE_OPTIONS = [
  { value: "athlete", label: "Athlete" },
  { value: "unified_partner", label: "Unified Partner" },
  { value: "caregiver", label: "Caregiver / Parent / Conservator" },
  { value: "coach", label: "Coach" },
  { value: "volunteer", label: "Volunteer" },
  { value: "partner", label: "Community Partner / Vendor / Venue" },
  { value: "donor", label: "Donor / Sponsor / Partner" },
  { value: "first_responder", label: "Law Enforcement or First Responder" },
  { value: "employment", label: "Interested in Employment / Internship" },
] as const satisfies readonly Option<InquiryRole>[];

// Step 4
export const TIMELINE_OPTIONS = [
  { value: "immediately", label: "Immediately" },
  { value: "30_days", label: "Within 30 days" },
  { value: "3_months", label: "Within 3 months" },
  { value: "exploring", label: "Just exploring" },
] as const;

export const INVOLVED_OPTIONS = [
  { value: "yes", label: "Yes" },
  { value: "no", label: "No" },
  { value: "unsure", label: "Unsure" },
] as const;

export const INTEREST_OPTIONS = [
  { value: "sports_competition", label: "Sports competition" },
  { value: "training", label: "Training & practice" },
  { value: "health_screenings", label: "Health screenings" },
  { value: "fitness", label: "Fitness programs" },
  { value: "athlete_leadership", label: "Athlete leadership" },
  { value: "events", label: "Event participation" },
] as const;

export const YES_NO_OPTIONS = [
  { value: "yes", label: "Yes" },
  { value: "no", label: "No" },
] as const;

// Step 5: athlete
export const DISABILITY_OPTIONS = [
  { value: "yes", label: "Yes" },
  { value: "not_sure", label: "Not sure" },
] as const;

export const SPORT_OPTIONS = [
  { value: "basketball", label: "Basketball" },
  { value: "bowling", label: "Bowling" },
  { value: "track_and_field", label: "Track & Field" },
  { value: "soccer", label: "Soccer" },
  { value: "swimming", label: "Swimming" },
  { value: "tennis", label: "Tennis" },
  { value: "bocce", label: "Bocce" },
  { value: "flag_football", label: "Flag Football" },
] as const;

export const LOOKING_FOR_OPTIONS = [
  { value: "training", label: "Training" },
  { value: "competition", label: "Competition" },
  { value: "both", label: "Both" },
] as const;

export const FREQUENCY_OPTIONS = [
  { value: "weekly", label: "Weekly" },
  { value: "monthly", label: "Monthly" },
  { value: "seasonal", label: "Seasonal" },
] as const;

export const COMPETITION_LEVEL_OPTIONS = [
  { value: "local", label: "Local" },
  { value: "regional", label: "Regional" },
  { value: "state", label: "State" },
  { value: "national", label: "National" },
] as const;

// Step 6
export const CONTACT_METHOD_OPTIONS = [
  { value: "email", label: "Email" },
  { value: "phone", label: "Phone" },
  { value: "text", label: "Text" },
] as const;

export type IntakeAnswers = {
  // Step 1
  whoFor?: ValueOf<typeof WHO_FOR_OPTIONS>;
  // Step 2
  role?: InquiryRole;
  // Step 3
  zipCode: string;
  // Step 4
  timeline?: ValueOf<typeof TIMELINE_OPTIONS>;
  currentlyInvolved?: ValueOf<typeof INVOLVED_OPTIONS>;
  interests: ValueOf<typeof INTEREST_OPTIONS>[];
  participatedBefore?: ValueOf<typeof YES_NO_OPTIONS>;
  accessibilityNeeds: string;
  // Step 5: athlete
  athleteAge: string; // text for input, converted to number on submit
  disability?: ValueOf<typeof DISABILITY_OPTIONS>;
  sports: ValueOf<typeof SPORT_OPTIONS>[];
  lookingFor?: ValueOf<typeof LOOKING_FOR_OPTIONS>;
  frequency?: ValueOf<typeof FREQUENCY_OPTIONS>;
  competitionLevel?: ValueOf<typeof COMPETITION_LEVEL_OPTIONS>;
  // Step 6
  contactName: string;
  contactEmail: string;
  contactPhone: string;
  contactMethod?: ValueOf<typeof CONTACT_METHOD_OPTIONS>;
  consent: boolean;
};

export const EMPTY_ANSWERS: IntakeAnswers = {
  zipCode: "",
  interests: [],
  accessibilityNeeds: "",
  athleteAge: "",
  sports: [],
  contactName: "",
  contactEmail: "",
  contactPhone: "",
  consent: false,
};

// Props every step component receives from the form.
export type StepProps = {
  answers: IntakeAnswers;
  update: <K extends keyof IntakeAnswers>(
    field: K,
    value: IntakeAnswers[K],
  ) => void;
};

export type IntakeStep = {
  // A function when the wording depends on earlier answers (e.g. "About you" vs "About the athlete").
  title: string | ((answers: IntakeAnswers) => string);
  Component: (props: StepProps) => ReactNode;
  isValid: (answers: IntakeAnswers) => boolean;
};

export const ZIP_PATTERN = /^\d{5}(-\d{4})?$/;
export const EMAIL_PATTERN = /^\S+@\S+\.\S+$/;

export const labelOf = <T extends string>(
  options: readonly Option<T>[],
  value: T | undefined,
) => options.find((option) => option.value === value)?.label ?? "—";

export const toInquiryCreate = (
  a: IntakeAnswers & { role: InquiryRole },
): InquiryCreate => ({
  role: a.role,
  contact_name: a.contactName.trim(),
  contact_email: a.contactEmail.trim() || null,
  contact_phone: a.contactPhone.trim() || null,
  zip_code: a.zipCode,
  answers: {
    who_for: a.whoFor,
    timeline: a.timeline,
    currently_involved: a.currentlyInvolved,
    interests: a.interests,
    participated_before: a.participatedBefore,
    accessibility_needs: a.accessibilityNeeds.trim() || null,
    preferred_contact_method: a.contactMethod,
    consent: a.consent,
    ...(a.role === "athlete" && {
      athlete: {
        age: Number(a.athleteAge),
        disability: a.disability,
        sports: a.sports,
        looking_for: a.lookingFor,
        frequency: a.frequency,
        competition_level: a.competitionLevel,
      },
    }),
  },
});
