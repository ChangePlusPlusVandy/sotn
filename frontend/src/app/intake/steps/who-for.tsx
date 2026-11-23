import { RadioField } from "../fields";
import { WHO_FOR_OPTIONS, type StepProps } from "../intake-types";

export const WhoForStep = ({ answers, update }: StepProps) => (
  <RadioField
    legend="Who is this for?"
    hideLegend
    options={WHO_FOR_OPTIONS}
    value={answers.whoFor}
    onChange={(value) => update("whoFor", value)}
  />
);
