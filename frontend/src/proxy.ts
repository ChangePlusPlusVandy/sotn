import { clerkMiddleware } from "@clerk/nextjs/server";

// Makes the Clerk session available to server code. It does not protect any routes:
// each protected page calls auth.protect() itself (see src/app/admin/page.tsx).
export default clerkMiddleware();

export const config = {
  matcher: [
    // Skip Next.js internals and static files.
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    "/(api|trpc)(.*)",
  ],
};
