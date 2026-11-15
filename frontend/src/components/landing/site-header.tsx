import Image from "next/image";

const SiteHeader = () => {
  return (
    <header className="flex items-center gap-3 px-5 pt-6 pb-[calc(100svh/8)] md:gap-4 md:px-16 md:py-6">
      <Image
        src="/train4life-logo.png"
        alt="Train4Life"
        width={1792}
        height={512}
        priority
        className="h-7 w-auto md:h-10"
      />
      <div className="h-7 w-px bg-neutral-400 md:h-8" />
      <p className="text-[10px] font-medium tracking-[0.2em] text-muted-foreground uppercase md:text-xs">
        Special Olympics
        <br />
        Tennessee
      </p>
    </header>
  );
};

export default SiteHeader;
