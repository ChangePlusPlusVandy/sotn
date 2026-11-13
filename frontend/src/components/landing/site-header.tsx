import Image from "next/image";

const SiteHeader = () => {
  return (
    <header className="flex items-center gap-4 px-8 py-6 md:px-16">
      <Image
        src="/train4life-logo.png"
        alt="Train4Life"
        width={1920}
        height={755}
        priority
        className="h-14 w-auto"
      />
      <div className="h-8 w-px bg-border" />
      <p className="text-xs font-medium tracking-[0.2em] text-muted-foreground uppercase">
        Special Olympics
        <br />
        Tennessee
      </p>
    </header>
  );
};

export default SiteHeader;
