"use client";

import { useRouter as useRouterNavigation } from "next/navigation";
import { useRouter } from "next/router";
import { useState, useEffect, Suspense } from "react";

import RootLayout from "@/components/layout";
import SearchResultItem from "@/components/search-result-item";
import SearchTop from "@/components/search-top";
import SkeletonLoader from "@/components/skeleton-search-result";

const fetchSearchResults = async (
  query: string,
  page: string | string[] | 1,
  s: string | string[] | undefined,
  r: string | string[] | undefined,
  d: string | string[] | undefined
) => {
  const res = await fetch(
    `/api/search?q=${query}&page=${page}&s=${s}&r=${r}&d=${d}`
  );
  return res.json();
};

const SearchPage: React.FC = () => {
  const [results, setResults] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const { q, s, r, d, page } = router.query;
  const routerNavigation = useRouterNavigation();

  useEffect(() => {
    const fetchResults = async () => {
      if (q) {
        if (!s || !r || !d || !page) {
          routerNavigation.push(
            `/search?q=${q}&s=${s || "DESC"}&r=${r || 100}&d=${d || "t"}&page=${
              page || 1
            }`
          );
        }
        setLoading(true);
        const data = await fetchSearchResults(
          q as string,
          page || 1,
          s || "DESC",
          r || '100',
          d || 't'
        );
        setResults(data.results);
        setTotal(data.total);
        setTotalPages(data.totalPages);

        if (data.totalPages < parseInt(page as string)) {
          router.replace(`/search?q=${q}&s=${s}&r=${r}&d=${d}&page=${1}`);
          return;
        }
        setCurrentPage(data.currentPage);
        setLoading(false);
      }
      console.log("load");
    };

    fetchResults();
  }, [q, currentPage, r, d, s, page]);

  return (
    <Suspense fallback={<SkeletonLoader />}>
      <RootLayout>
        <main className="bg-white w-full h-full min-h-screen max-h-screen overflow-hidden flex flex-col">
          {loading ? (
            <SkeletonLoader />
          ) : (
            <>
              <SearchTop
                currentPage={currentPage}
                totalPages={totalPages}
                totalResults={total}
              />
              <section className="pl-12 py-4 flex flex-col gap-2 overflow-y-scroll">
                {Array.isArray(results) &&
                  results.map((result, index) => (
                    <SearchResultItem key={index} result={result} />
                  ))}
              </section>
            </>
          )}
        </main>
      </RootLayout>
    </Suspense>
  );
};

export default SearchPage;
