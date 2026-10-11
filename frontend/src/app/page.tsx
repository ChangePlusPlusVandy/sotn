import Link from "next/link";

const Home = () => {
  return (
    <main className="flex flex-col gap-4 p-8">
      <h1 className="text-2xl font-semibold">SOTN / Train4Life</h1>
      <p>TODO: Landing page with a Start Intake button.</p>
      <Link href="/intake" className="underline">
        Start intake
      </Link>
    </main>
  );
};

export default Home;
