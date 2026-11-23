import { Label } from "@/components/ui/label";

import { CheckboxGroupField, RadioField } from "../fields";
import {
  INTEREST_OPTIONS,
  INVOLVED_OPTIONS,
  TIMELINE_OPTIONS,
  YES_NO_OPTIONS,
  type StepProps,
} from "../intake-types";

export const QuickQuestionsStep = ({ answers, update }: StepProps) => (
  <div className="flex flex-col gap-8">
    <RadioField
      legend="How soon are you looking to get involved?"
      options={TIMELINE_OPTIONS}
      value={answers.timeline}
      onChange={(value) => update("timeline", value)}
    />
    <RadioField
      legend="Are you currently involved with Special Olympics Tennessee?"
      options={INVOLVED_OPTIONS}
      value={answers.currentlyInvolved}
      onChange={(value) => update("currentlyInvolved", value)}
    />
    <CheckboxGroupField
      legend="What are you most interested in today? (Select all that apply)"
      options={INTEREST_OPTIONS}
      value={answers.interests}
      onChange={(value) => update("interests", value)}
    />
    <RadioField
      legend="Have you participated in Special Olympics before?"
      options={YES_NO_OPTIONS}
      value={answers.participatedBefore}
      onChange={(value) => update("participatedBefore", value)}
    />
    <div className="flex flex-col gap-2">
      <Label htmlFor="accessibility-needs">
        Any accessibility, communication or support needs we should know about?
        (Optional)
      </Label>
      <textarea
        id="accessibility-needs"
        rows={3}
        placeholder="e.g. ASL interpreter, wheelchair access, sensory considerations"
        className="rounded-md border border-input bg-transparent px-2.5 py-2 text-sm shadow-xs outline-none placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
        value={answers.accessibilityNeeds}
        onChange={(event) => update("accessibilityNeeds", event.target.value)}
      />
    </div>
  </div>
);
