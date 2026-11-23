"use client";

import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";

import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { api } from "@/lib/api";

import {
  EMAIL_PATTERN,
  EMPTY_ANSWERS,
  ZIP_PATTERN,
  toInquiryCreate,
  type InquiryRole,
  type IntakeAnswers,
  type IntakeStep,
  type StepProps,
} from "./intake-types";
import { AboutAthleteStep } from "./steps/about-athlete";
import { ContactStep } from "./steps/contact";
import { LocationStep } from "./steps/location";
import { QuickQuestionsStep } from "./steps/quick-questions";
import { ReviewStep } from "./steps/review";
import { RoleStep } from "./steps/role";
import { WhoForStep } from "./steps/who-for";

const WHO_FOR: IntakeStep = {
  title: "Who is this for?",
  Component: WhoForStep,
  isValid: (a) => a.whoFor !== undefined,
};

const ROLE: IntakeStep = {
  title: "Which best describes you?",
  Component: RoleStep,
  isValid: (a) => a.role !== undefined,
};

const LOCATION: IntakeStep = {
  title: "Where do you live or work?",
  Component: LocationStep,
  isValid: (a) => ZIP_PATTERN.test(a.zipCode),
};

const QUICK_QUESTIONS: IntakeStep = {
  title: "A few quick questions",
  Component: QuickQuestionsStep,
  isValid: (a) =>
    a.timeline !== undefined &&
    a.currentlyInvolved !== undefined &&
    a.participatedBefore !== undefined,
};

const CONTACT: IntakeStep = {
  title: "How can we reach you?",
  Component: ContactStep,
  isValid: (a) => {
    const email = a.contactEmail.trim();
    const phone = a.contactPhone.trim();
    return (
      a.contactName.trim() !== "" &&
      // The backend requires an email or phone number.
      (email !== "" || phone !== "") &&
      (email === "" || EMAIL_PATTERN.test(email)) &&
      a.contactMethod !== undefined &&
      // Phone and text need a phone number to reach.
      (a.contactMethod === "email" ? email !== "" : phone !== "") &&
      a.consent
    );
  },
};

const REVIEW: IntakeStep = {
  title: "Check your answers",
  Component: ReviewStep,
  isValid: () => true,
};

const ROLE_STEPS: Partial<Record<InquiryRole, IntakeStep>> = {
  athlete: {
    title: (a) =>
      a.whoFor === "someone_else" ? "About the athlete" : "About you",
    Component: AboutAthleteStep,
    isValid: (a) => {
      const age = Number(a.athleteAge);
      return (
        Number.isInteger(age) &&
        age >= 1 &&
        age <= 120 &&
        a.disability !== undefined
      );
    },
  },
};

const getSteps = (answers: IntakeAnswers): IntakeStep[] => {
  const roleStep = answers.role ? ROLE_STEPS[answers.role] : undefined;
  return [
    WHO_FOR,
    ROLE,
    LOCATION,
    QUICK_QUESTIONS,
    ...(roleStep ? [roleStep] : []),
    CONTACT,
    REVIEW,
  ];
};

export const IntakeForm = () => {
  const router = useRouter();
  const [answers, setAnswers] = useState<IntakeAnswers>(EMPTY_ANSWERS);
  const [stepIndex, setStepIndex] = useState(0);
  const [status, setStatus] = useState<"idle" | "submitting" | "error">("idle");
  const headingRef = useRef<HTMLHeadingElement>(null);
  const hasNavigated = useRef(false);

  const steps = getSteps(answers);
  // Changing the role can remove step 5, so keep the index in range.
  const index = Math.min(stepIndex, steps.length - 1);
  const step = steps[index];
  const isLast = index === steps.length - 1;
  const StepComponent = step.Component;
  const title =
    typeof step.title === "function" ? step.title(answers) : step.title;

  // Move focus to the new step's heading so screen readers announce it.
  useEffect(() => {
    if (hasNavigated.current) headingRef.current?.focus();
  }, [index]);

  const update: StepProps["update"] = (field, value) =>
    setAnswers((prev) => ({ ...prev, [field]: value }));

  const goTo = (next: number) => {
    hasNavigated.current = true;
    setStepIndex(next);
  };

  const submit = async (role: InquiryRole) => {
    setStatus("submitting");
    try {
      const { error } = await api.POST("/inquiries", {
        body: toInquiryCreate({ ...answers, role }),
      });
      if (error) throw error;
    } catch {
      setStatus("error");
      return;
    }
    router.push(`/results?role=${role}`);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!step.isValid(answers) || status === "submitting") return;
    if (isLast) {
      if (answers.role) submit(answers.role);
      return;
    }
    goTo(index + 1);
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-6">
      <div className="flex flex-col gap-2">
        <p className="text-sm text-muted-foreground">
          Step {index + 1} of {steps.length}
        </p>
        <Progress value={((index + 1) / steps.length) * 100} />
      </div>

      <h2
        ref={headingRef}
        tabIndex={-1}
        className="text-xl font-semibold outline-none"
      >
        {title}
      </h2>

      <StepComponent answers={answers} update={update} />

      {status === "error" && (
        <p role="alert" className="text-sm text-destructive">
          Something went wrong sending your answers. Please try again.
        </p>
      )}

      <div className="flex justify-between">
        <Button
          type="button"
          variant="outline"
          onClick={() => goTo(index - 1)}
          disabled={index === 0 || status === "submitting"}
        >
          Back
        </Button>
        <Button
          type="submit"
          disabled={!step.isValid(answers) || status === "submitting"}
        >
          {isLast
            ? status === "submitting"
              ? "Submitting…"
              : "Submit"
            : "Next"}
        </Button>
      </div>
    </form>
  );
};
