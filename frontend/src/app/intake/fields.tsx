"use client";

import { useId } from "react";

import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";

import type { Option } from "./intake-types";

type FieldProps = {
  legend: string;
  hideLegend?: boolean;
};

export const RadioField = <T extends string>({
  legend,
  hideLegend,
  options,
  value,
  onChange,
}: FieldProps & {
  options: readonly Option<T>[];
  value: T | undefined;
  onChange: (value: T) => void;
}) => {
  const id = useId();

  return (
    <fieldset className="flex flex-col gap-3">
      <legend className={hideLegend ? "sr-only" : "mb-3 font-medium"}>
        {legend}
      </legend>
      <RadioGroup
        value={value ?? ""}
        onValueChange={(next) => onChange(next as T)}
      >
        {options.map((option) => (
          <div key={option.value} className="flex items-center gap-2">
            <RadioGroupItem id={`${id}-${option.value}`} value={option.value} />
            <Label htmlFor={`${id}-${option.value}`}>{option.label}</Label>
          </div>
        ))}
      </RadioGroup>
    </fieldset>
  );
};

export const CheckboxGroupField = <T extends string>({
  legend,
  hideLegend,
  options,
  value,
  onChange,
}: FieldProps & {
  options: readonly Option<T>[];
  value: T[];
  onChange: (value: T[]) => void;
}) => {
  const id = useId();

  return (
    <fieldset className="flex flex-col gap-3">
      <legend className={hideLegend ? "sr-only" : "mb-3 font-medium"}>
        {legend}
      </legend>
      {options.map((option) => (
        <div key={option.value} className="flex items-center gap-2">
          <Checkbox
            id={`${id}-${option.value}`}
            checked={value.includes(option.value)}
            onCheckedChange={(checked) =>
              onChange(
                checked === true
                  ? [...value, option.value]
                  : value.filter((selected) => selected !== option.value),
              )
            }
          />
          <Label htmlFor={`${id}-${option.value}`}>{option.label}</Label>
        </div>
      ))}
    </fieldset>
  );
};
