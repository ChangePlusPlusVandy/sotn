import { Suspense } from "react";
import Link from "next/link";
import { UserButton } from "@clerk/nextjs";

const NAV = [
  { href: "/admin", label: "Dashboard" },
  { href: "/admin/triage", label: "Intake triage" },
  { href: "/admin/contacts", label: "Contacts" },
  { href: "/admin/follow-ups", label: "Follow-ups" },
  { href: "/admin/resources", label: "Resources" },
] as const;

// Navigation only. Layouts don't re-run on client navigation, so each admin page
// calls auth.protect() itself rather than relying on a check here. Reading the session
// is request-time work, so pages render inside <Suspense> while the nav prerenders.
const AdminLayout = ({ children }: LayoutProps<"/admin">) => {
  return (
    <div className="flex flex-1">
      <nav className="flex w-56 flex-col gap-2 border-r p-4">
        {NAV.map(({ href, label }) => (
          <Link key={href} href={href}>
            {label}
          </Link>
        ))}
        <div className="mt-auto">
          <UserButton />
        </div>
      </nav>
      <main className="flex-1 p-8">
        <Suspense fallback={<p>Loading...</p>}>{children}</Suspense>
      </main>
    </div>
  );
};

export default AdminLayout;
