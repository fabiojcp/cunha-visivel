import { useRouter, useSearchParams, usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import data from "@/database/db.json"; // Importe os dados de db.json
import { Data, PaginatedResults, SearchResult } from "@/types";

// Definição das interfaces diretamente no arquivo


const RESULTS_PER_PAGE = 10;
const SUBSTRING_LENGTH = 200;

export const useSearchResults = () => {
  const [results, setResults] = useState<PaginatedResults>({
    results: [],
    total: 0,
    currentPage: 1,
    totalPages: 0,
  });
  const searchParams = useSearchParams();
  const search = searchParams?.get("q");
  const router = useRouter();
  const pathname = usePathname();
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    if (!search) {
      router.push("/");
    } else {
      const searchResults: SearchResult[] = [];

      const jsonData = data as unknown as Data;

      for (const link in jsonData.pdf_links) {
        const pdf = jsonData.pdf_links[link];
        pdf.pages.forEach((page) => {
          if (page.text.toLowerCase().includes(search.toLowerCase())) {
            const startIndex = page.text
              .toLowerCase()
              .indexOf(search.toLowerCase());
            const snippetStart = Math.max(startIndex - SUBSTRING_LENGTH, 0);
            const snippetEnd = Math.min(
              startIndex + search.length + SUBSTRING_LENGTH,
              page.text.length
            );
            const snippet = page.text.substring(snippetStart, snippetEnd);

            searchResults.push({
              page: page.number,
              snippet,
              link,
              name: pdf.name,
              date: pdf.date,
              year: pdf.year,
              edition: pdf.edition,
            });
          }
        });
      }

      const total = searchResults.length;
      const totalPages = Math.ceil(total / RESULTS_PER_PAGE);
      const paginatedResults = searchResults.slice(
        (currentPage - 1) * RESULTS_PER_PAGE,
        currentPage * RESULTS_PER_PAGE
      );

      setResults({
        results: paginatedResults,
        total,
        currentPage,
        totalPages,
      });
    }
  }, [router, search, pathname, currentPage]);

  const updatePage = (page: number) => {
    setCurrentPage(page);
  };

  return { results, updatePage };
};
