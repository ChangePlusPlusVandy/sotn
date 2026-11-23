import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import { RadioField } from "../fields";
import { CONTACT_METHOD_OPTIONS, type StepProps } from "../intake-types";

export const ContactStep = ({ answers, update }: StepProps) => (
  <div className="flex flex-col gap-6">
    <div className="flex flex-col gap-2">
      <Label htmlFor="contact-name">Full name</Label>
      <Input
        id="contact-name"
        autoComplete="name"
        maxLength={200}
        value={answers.contactName}
        onChange={(event) => update("contactName", event.target.value)}
      />
    </div>
    <div className="flex flex-col gap-2">
      <Label htmlFor="contact-email">Email</Label>
      <Input
        id="contact-email"
        type="email"
        autoComplete="email"
        maxLength={320}
        value={answers.contactEmail}
        onChange={(event) => update("contactEmail", event.target.value)}
      />
    </div>
    <div className="flex flex-col gap-2">
      <Label htmlFor="contact-phone">Phone (optional)</Label>
      <Input
        id="contact-phone"
        type="tel"
        autoComplete="tel"
        maxLength={32}
        value={answers.contactPhone}
        onChange={(event) => update("contactPhone", event.target.value)}
      />
    </div>
    <RadioField
      legend="Preferred method of communication"
      options={CONTACT_METHOD_OPTIONS}
      value={answers.contactMethod}
      onChange={(value) => update("contactMethod", value)}
    />
    <div className="flex items-center gap-2">
      <Checkbox
        id="consent"
        checked={answers.consent}
        onCheckedChange={(checked) => update("consent", checked === true)}
      />
      <Label htmlFor="consent">
        It&apos;s OK to contact me about next steps
      </Label>
    </div>
  </div>
);
