import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import { CheckboxGroupField, RadioField } from "../fields";
import {
  COMPETITION_LEVEL_OPTIONS,
  DISABILITY_OPTIONS,
  FREQUENCY_OPTIONS,
  LOOKING_FOR_OPTIONS,
  SPORT_OPTIONS,
  type StepProps,
} from "../intake-types";

export const AboutAthleteStep = ({ answers, update }: StepProps) => {
  // Reword the questions when someone is filling this in for the athlete.
  const forSomeoneElse = answers.whoFor === "someone_else";

  return (
    <div className="flex flex-col gap-8">
      <div className="flex flex-col gap-2">
        <Label htmlFor="athlete-age">
          {forSomeoneElse ? "Athlete's age" : "Your age"}
        </Label>
        <Input
          id="athlete-age"
          type="number"
          inputMode="numeric"
          min={1}
          max={120}
          className="w-24"
          value={answers.athleteAge}
          onChange={(event) => update("athleteAge", event.target.value)}
        />
      </div>
      <RadioField
        legend={
          forSomeoneElse
            ? "Does the athlete have an intellectual or developmental disability?"
            : "Do you have an intellectual or developmental disability?"
        }
        options={DISABILITY_OPTIONS}
        value={answers.disability}
        onChange={(value) => update("disability", value)}
      />
      <CheckboxGroupField
        legend="Sports of interest"
        options={SPORT_OPTIONS}
        value={answers.sports}
        onChange={(value) => update("sports", value)}
      />
      <RadioField
        legend={
          forSomeoneElse
            ? "Is the athlete looking for…"
            : "Are you looking for…"
        }
        options={LOOKING_FOR_OPTIONS}
        value={answers.lookingFor}
        onChange={(value) => update("lookingFor", value)}
      />
      <RadioField
        legend={
          forSomeoneElse
            ? "How often would the athlete like to participate?"
            : "How often would you like to participate?"
        }
        options={FREQUENCY_OPTIONS}
        value={answers.frequency}
        onChange={(value) => update("frequency", value)}
      />
      <RadioField
        legend="Competition level of interest"
        options={COMPETITION_LEVEL_OPTIONS}
        value={answers.competitionLevel}
        onChange={(value) => update("competitionLevel", value)}
      />
    </div>
  );
};
