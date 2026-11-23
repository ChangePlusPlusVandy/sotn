import { IntakeForm } from "./intake-form";

const IntakePage = () => {
  return (
    <main className="mx-auto flex w-full max-w-xl flex-col gap-6 p-8">
      <h1 className="text-2xl font-semibold">Get involved</h1>
      <IntakeForm />
    </main>
  );
};

export default IntakePage;
