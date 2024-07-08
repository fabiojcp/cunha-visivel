export const maxDuration = 1000;
export const dynamic = "force-dynamic";

import type { NextApiRequest, NextApiResponse } from "next";
import { SearchResult } from "@/types";
import { PrismaClient } from "@prisma/client";
import { paginateResults } from "@/utils/pagination";

const RESULTS_PER_PAGE = "100";
const SUBSTRING_LENGTH = 200;

export default async function Search(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const prisma = new PrismaClient();
  const query = req.query.q as string;
  const page = parseInt(req.query.page as string) || 1;

  function filterQuery(
    query: string | string[] | undefined,
    defaultValue: string | number | boolean
  ) {
    if (query && query !== "undefined") {
      return typeof query === "string" && query.length ? query : defaultValue;
    }
    return defaultValue;
  }

  if (!query) {
    return res.status(400).json({ error: "Query is required" });
  }
  const sort = filterQuery(req.query.s, "DESC");
  const result = parseInt(filterQuery(req.query.r, RESULTS_PER_PAGE) as string);
  const removeDuplicates = filterQuery(req.query.d, false) === "t";

  const pages = await prisma.page.findMany({
    where: {
      text: {
        contains: query,
      },
    },
    include: {
      pdfLink: {
        select: {
          name: true,
          date: true,
          year: true,
          edition: true,
          url: true,
        },
      },
    },
  });

  // Process search results
  let searchResults: SearchResult[] = pages.map((page) => {
    const startIndex = page.text.toLowerCase().indexOf(query.toLowerCase());
    const snippetStart = Math.max(startIndex - SUBSTRING_LENGTH, 0);
    const snippetEnd = Math.min(
      startIndex + query.length + SUBSTRING_LENGTH,
      page.text.length
    );
    const snippet = page.text.substring(snippetStart, snippetEnd);

    return {
      page: page.number,
      snippet,
      link: page.pdfLink?.url || "",
      name: page?.pdfLink?.name || "",
      date: page?.pdfLink?.date || "",
      year: page?.pdfLink?.year || "",
      edition: page?.pdfLink?.edition || "",
    };
  });

  if (!removeDuplicates) {
    const uniqueResults: SearchResult[] = [];
    const linksSeen = new Set();

    searchResults.forEach((result) => {
      if (!linksSeen.has(result.link)) {
        uniqueResults.push(result);
        linksSeen.add(result.link);
      }
    });

    searchResults = uniqueResults;
  }

  searchResults.sort((a, b) => {
    const editionA = parseInt(a.edition, 10);
    const editionB = parseInt(b.edition, 10);

    if (sort === "ASC") {
      return editionA - editionB;
    } else {
      return editionB - editionA;
    }
  });

  const { paginatedResults, total, totalPages, currentPage } = paginateResults(
    searchResults,
    page,
    result
  );

  res
    .status(200)
    .json({ results: paginatedResults, total, totalPages, currentPage });
}
