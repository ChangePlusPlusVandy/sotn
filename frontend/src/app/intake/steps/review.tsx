import {
  COMPETITION_LEVEL_OPTIONS,
  CONTACT_METHOD_OPTIONS,
  DISABILITY_OPTIONS,
  FREQUENCY_OPTIONS,
  INTEREST_OPTIONS,
  INVOLVED_OPTIONS,
  LOOKING_FOR_OPTIONS,
  ROLE_OPTIONS,
  SPORT_OPTIONS,
  TIMELINE_OPTIONS,
  WHO_FOR_OPTIONS,
  YES_NO_OPTIONS,
  labelOf,
  type Option,
  type StepProps,
} from "../intake-types";

const labelsOf = <T extends string>(
  options: readonly Option<T>[],
  values: T[],
) =>
  values.length
    ? values.map((value) => labelOf(options, value)).join(", ")
    : "—";

export const ReviewStep = ({ answers: a }: StepProps) => {
  const rows: [string, string][] = [
    ["Who is this for?", labelOf(WHO_FOR_OPTIONS, a.whoFor)],
    ["Role", labelOf(ROLE_OPTIONS, a.role)],
    ["ZIP code", a.zipCode],
    ["How soon", labelOf(TIMELINE_OPTIONS, a.timeline)],
    ["Currently involved", labelOf(INVOLVED_OPTIONS, a.currentlyInvolved)],
    ["Interests", labelsOf(INTEREST_OPTIONS, a.interests)],
    ["Participated before", labelOf(YES_NO_OPTIONS, a.participatedBefore)],
    ["Accessibility needs", a.accessibilityNeeds.trim() || "—"],
    ...(a.role === "athlete"
      ? ([
          ["Age", a.athleteAge],
          [
            "Intellectual or developmental disability",
            labelOf(DISABILITY_OPTIONS, a.disability),
          ],
          ["Sports", labelsOf(SPORT_OPTIONS, a.sports)],
          ["Looking for", labelOf(LOOKING_FOR_OPTIONS, a.lookingFor)],
          ["How often", labelOf(FREQUENCY_OPTIONS, a.frequency)],
          [
            "Competition level",
            labelOf(COMPETITION_LEVEL_OPTIONS, a.competitionLevel),
          ],
        ] satisfies [string, string][])
      : []),
    ["Name", a.contactName],
    ["Email", a.contactEmail || "—"],
    ["Phone", a.contactPhone || "—"],
    ["Preferred contact", labelOf(CONTACT_METHOD_OPTIONS, a.contactMethod)],
  ];

  return (
    <div className="flex flex-col gap-4">
      <p className="text-muted-foreground">
        Use Back to change anything before you submit.
      </p>
      <dl className="grid grid-cols-[auto_1fr] gap-x-6 gap-y-2 text-sm">
        {rows.map(([label, value]) => (
          <div key={label} className="contents">
            <dt className="text-muted-foreground">{label}</dt>
            <dd>{value}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
};
