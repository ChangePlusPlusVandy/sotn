// All the text and links on the results page, so wording can change in one place.
// The wording comes from the Figma design (Questionnaire v2, "intake-8-submitted").

export const CONTENT = {
  heading: "Thanks! You’re all set.",
  subheading: "A coordinator will reach out within 2 business days.",
  programs: {
    label: "Programs that fit you",
    intro: "Optional: answer a few more questions so we can help you faster.",
    start: "Start",
    loadError: "We couldn’t load program suggestions right now. Please try again later.",
  },
  nextSteps: {
    label: "What happens next",
    steps: [
      "We review your answers (1–2 days)",
      "A coordinator near you reaches out",
      "Track your progress in your resource portal",
    ],
  },
  portal: "Go to your resource portal",
} as const;

export const LINKS = {
  // TODO: the resource portal page doesn't exist yet.
  portal: "/portal",
  // TODO: the per-program questionnaires don't exist yet, so Start goes to the intake form.
  startProgram: "/intake",
} as const;
