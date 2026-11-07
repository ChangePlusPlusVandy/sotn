"use client";

import { useAuth } from "@clerk/nextjs";
import { useMemo } from "react";
import { createAuthedApi } from "./api";

export const useApi = () => {
  const { getToken } = useAuth();
  return useMemo(() => createAuthedApi(getToken), [getToken]);
};
