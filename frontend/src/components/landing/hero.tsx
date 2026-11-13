import type { ReactNode } from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

type HeroProps = {
  heading: ReactNode;
  description: string;
  ctaLabel: string;
  ctaHref: string;
};

const Hero = ({ heading, description, ctaLabel, ctaHref }: HeroProps) => {
  return (
    <div className="flex flex-col items-start gap-8">
      <h1 className="text-5xl leading-tight font-bold tracking-tight text-neutral-900 md:text-6xl">
        {heading}
      </h1>
      <p className="max-w-xl text-lg text-muted-foreground">{description}</p>
      <Button
        asChild
        size="lg"
        className="h-12 gap-3 rounded-lg bg-brand px-6 text-base text-white hover:bg-brand/90"
      >
        <Link href={ctaHref}>
          {ctaLabel}
          <ArrowRight />
        </Link>
      </Button>
    </div>
  );
};

export default Hero;
