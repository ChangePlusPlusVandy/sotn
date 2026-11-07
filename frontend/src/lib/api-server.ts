import { auth } from "@clerk/nextjs/server";
import { createAuthedApi } from "./api";

export const getServerApi = async () => {
  const { getToken } = await auth();
  return createAuthedApi(getToken);
};
