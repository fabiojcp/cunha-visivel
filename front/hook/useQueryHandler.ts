"use client";

import { useRouter, useSearchParams, usePathname } from "next/navigation";
import { useCallback, useEffect } from "react";

import { useQueryStore } from "../store/useQueryStore";

export const useQueryHandler = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const actualPathname = usePathname();
  const setSearchParams = useQueryStore((state) => state.setSearchParams);
  const s = searchParams?.get("s") || "ASC";
  const r = searchParams?.get("r") || "100";
  const d = searchParams?.get("d") || "t";


  useEffect(() => {
    setSearchParams(new URLSearchParams(searchParams?.toString()));
  }, [searchParams, setSearchParams]);

  const createQueryString = useCallback(
    (name: string, value: string, pathname: string | null = actualPathname) => {
      const params = new URLSearchParams(searchParams?.toString());
      params.set(name, value);

      const newParams = params.toString();
      router.push(pathname + "?" + newParams);
      setSearchParams(params);
    },
    [actualPathname, router, searchParams, setSearchParams]
  );

  return { createQueryString, searchParams };
};
