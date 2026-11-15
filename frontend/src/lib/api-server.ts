import { auth } from "@clerk/nextjs/server";
import { connection } from "next/server";
import { createAuthedApi } from "./api";

export const getServerApi = async () => {
  await connection();
  const { getToken } = await auth();
  return createAuthedApi(getToken);
};
