"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV_ITEMS = [
  { label: "Home", href: "/portal" },
  { label: "Programs", href: "/portal/programs" },
  { label: "Resources", href: "/portal/resources" },
  { label: "Events", href: "/portal/events" },
  { label: "Messages", href: "/portal/messages" },
  { label: "My profile", href: "/portal/profile" },
];

export const PortalSidebar = () => {
  const pathname = usePathname();

  return (
    <aside className="flex w-64 shrink-0 flex-col justify-between bg-[#ECE8DC] p-6">
      <div className="flex flex-col gap-6">
        <div>
          {/* TODO: swap in the team's logo image if there's one in /public */}
          <p className="text-xs font-bold italic">Special Olympics</p>
          <h2 className="mt-3 text-xl font-semibold">Resource Portal</h2>
          <p className="text-xs text-gray-600">
            Your programs, materials, and next steps.
          </p>
        </div>

        <nav className="flex flex-col gap-2">
          {NAV_ITEMS.map((item) => {
            const isActive =
              item.href === "/portal"
                ? pathname === "/portal"
                : pathname.startsWith(item.href);

            return (
              <Link
                key={item.href}
                href={item.href}
                aria-current={isActive ? "page" : undefined}
                className={`rounded-md border px-3 py-2 text-sm ${
                  isActive
                    ? "border-black bg-black text-white"
                    : "border-gray-200 bg-white hover:bg-gray-50"
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* TODO: replace with the signed-in user's name and role */}
      <div className="rounded-md border border-gray-200 bg-white px-3 py-2">
        <p className="text-sm font-medium">Aisha Robinson</p>
        <p className="text-xs text-gray-600">Athlete · East TN</p>
      </div>
    </aside>
  );
};