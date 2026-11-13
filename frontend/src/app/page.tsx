import { ShieldCheck, Sparkles, Users } from "lucide-react";
import Hero from "@/components/landing/hero";
import SiteHeader from "@/components/landing/site-header";
import Steps, { type Step } from "@/components/landing/steps";

const STEPS: Step[] = [
  {
    title: "Tell us about you",
    description: "About 5 minutes.",
    icon: <Users />,
  },
  {
    title: "See your matches",
    description: "Programs that fit you.",
    icon: <Sparkles />,
  },
  {
    title: "Hear from a real person",
    description: "A coordinator reaches out within 2 business days.",
    icon: <ShieldCheck />,
  },
];

const Home = () => {
  return (
    <>
      <SiteHeader />
      <main className="grid flex-1 items-center gap-16 px-8 pb-24 md:grid-cols-2 md:px-16">
        <Hero
          heading={
            <>
              Get involved with{" "}
              <span className="text-brand">Special Olympics Tennessee.</span>
            </>
          }
          description="Answer a few quick questions. We'll connect you with the right program and people."
          ctaLabel="Get started"
          ctaHref="/intake"
        />
        <Steps steps={STEPS} />
      </main>
    </>
  );
};

export default Home;
