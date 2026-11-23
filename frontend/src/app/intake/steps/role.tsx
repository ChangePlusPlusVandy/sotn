import { RadioField } from "../fields";
import { ROLE_OPTIONS, type StepProps } from "../intake-types";

export const RoleStep = ({ answers, update }: StepProps) => (
  <RadioField
    legend="Which best describes you?"
    hideLegend
    options={ROLE_OPTIONS}
    value={answers.role}
    onChange={(value) => update("role", value)}
  />
);
