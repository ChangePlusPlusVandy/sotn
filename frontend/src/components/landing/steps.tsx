import type { ReactNode } from "react";

export type Step = {
  title: string;
  description: string;
  // Optional until the icon set is supplied; the red tile renders either way.
  icon?: ReactNode;
};

const Steps = ({ steps }: { steps: Step[] }) => {
  return (
    <ol className="flex flex-col gap-8">
      {steps.map((step, index) => (
        <li key={step.title} className="flex items-center gap-4">
          <div className="flex size-14 shrink-0 items-center justify-center rounded-xl bg-brand text-white [&_svg]:size-6">
            {step.icon}
          </div>
          <div>
            <p className="font-bold text-neutral-900">
              {index + 1}. {step.title}
            </p>
            <p className="text-muted-foreground">{step.description}</p>
          </div>
        </li>
      ))}
    </ol>
  );
};

export default Steps;
