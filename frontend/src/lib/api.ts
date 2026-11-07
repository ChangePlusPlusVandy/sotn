import createClient from "openapi-fetch";
import type { paths } from "./api-types";

const baseUrl = process.env.NEXT_PUBLIC_API_URL;

// Public routes (no auth needed)
export const api = createClient<paths>({ baseUrl });

// Staff routes (attaches Clerk session token)
export const createAuthedApi = (getToken: () => Promise<string | null>) => {
  const client = createClient<paths>({ baseUrl });
  client.use({
    async onRequest({ request }) {
      const token = await getToken();
      if (token) request.headers.set("Authorization", `Bearer ${token}`);
      return request;
    },
  });
  return client;
};
