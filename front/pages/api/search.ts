import type { NextApiRequest, NextApiResponse } from "next";

import data from "@/database/db.json";
import { Data, SearchResult } from "@/types";

const RESULTS_PER_PAGE = "100";
const SUBSTRING_LENGTH = 200;

export default function Search(req: NextApiRequest, res: NextApiResponse) {
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
  const sort = filterQuery(req.query.s, "DESC");
  const result = filterQuery(req.query.r, RESULTS_PER_PAGE);
  const removeDuplicates = filterQuery(req.query.d, false) === "t";

  if (!query) {
    return res.status(400).json({ error: "Query is required" });
  }

  let searchResults: SearchResult[] = [];
  const jsonData = data as unknown as Data;

  for (const link in jsonData.pdf_links) {
    const pdf = jsonData.pdf_links[link];
    pdf.pages.forEach((page) => {
      if (page.text.toLowerCase().includes(query.toLowerCase())) {
        const startIndex = page.text.toLowerCase().indexOf(query.toLowerCase());
        const snippetStart = Math.max(startIndex - SUBSTRING_LENGTH, 0);
        const snippetEnd = Math.min(
          startIndex + query.length + SUBSTRING_LENGTH,
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

  if (sort === "ASC") {
    searchResults.sort((a, b) => Number(a.edition) - Number(b.edition));
  } else if (sort === "DESC") {
    searchResults.sort((a, b) => Number(b.edition) - Number(a.edition));
  }

  const total = searchResults.length;
  const totalPages = Math.ceil(total / parseInt(result as string));
  const paginatedResults = searchResults.slice(
    (page - 1) * parseInt(result as string),
    page * parseInt(result as string)
  );

  res.status(200).json({ results: paginatedResults, total, totalPages, page });
}
