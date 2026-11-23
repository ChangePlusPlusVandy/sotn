import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import { ZIP_PATTERN, type StepProps } from "../intake-types";

// TODO: switch to region / county / city
export const LocationStep = ({ answers, update }: StepProps) => {
  const showError =
    answers.zipCode !== "" && !ZIP_PATTERN.test(answers.zipCode);

  return (
    <div className="flex flex-col gap-2">
      <Label htmlFor="zip-code">ZIP code</Label>
      <Input
        id="zip-code"
        inputMode="numeric"
        autoComplete="postal-code"
        maxLength={10}
        value={answers.zipCode}
        onChange={(event) => update("zipCode", event.target.value.trim())}
        aria-invalid={showError}
        aria-describedby={showError ? "zip-code-error" : undefined}
      />
      {showError && (
        <p id="zip-code-error" className="text-sm text-destructive">
          Enter a 5-digit ZIP code.
        </p>
      )}
    </div>
  );
};
