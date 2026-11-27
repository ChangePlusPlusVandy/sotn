import Image from "next/image";
import Link from "next/link";

// Header for the public pages: Train4Life logo on the left, a link home on the right.
export const SiteHeader = () => {
  return (
    <header className="border-b border-line bg-white/60">
      <div className="mx-auto flex max-w-[1152px] items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-3">
          <Image
            src="/train4life-logo.png"
            alt="Train4Life"
            width={86}
            height={34}
            priority
          />
          <span className="border-l border-line pl-3 text-[10px] leading-[15px] font-medium tracking-[1.9px] text-ink-muted uppercase">
            Special Olympics
            <br />
            Tennessee
          </span>
        </Link>
        <Link href="/" className="shrink-0 text-sm whitespace-nowrap text-ink-muted hover:text-ink">
          Back to home
        </Link>
      </div>
    </header>
  );
};
