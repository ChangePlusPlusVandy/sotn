import type { ReactNode } from "react";
import { PortalSidebar } from "./portal-sidebar";

const PortalLayout = ({ children }: { children: ReactNode }) => {
  return (
    <div className="flex min-h-screen bg-white">
      <PortalSidebar />
      <main className="flex-1 px-10 py-8">{children}</main>
    </div>
  );
};

export default PortalLayout;