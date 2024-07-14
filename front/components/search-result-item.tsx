"use client";

import { useQueryHandler } from "@/hook/useQueryHandler";
import { SearchResult } from "@/types";

const highlightQuery = (text: string, query: string) => {
  const regex = new RegExp(`(${query})`, "gi");
  return text.replace(regex, "<strong class='font-black'>$1</strong>");
};

const SearchResultItem: React.FC<{ result: SearchResult }> = ({ result }) => {
  const { searchParams } = useQueryHandler();
  const search = searchParams?.get("q");

  const highlightedSnippet = highlightQuery(result.snippet, search as string);

  return (
    <article className="mb-5 flex flex-col gap-0.5">
      <a
        href={result.link}
        target="_blank"
        className="text-blue-600 text-lg font-medium hover:underline"
      >
        {result.name}
      </a>
      <section className="text-sm text-gray-600 flex gap-2">
        <p>Página: {result.page}</p>
      </section>
      <section className="text-sm text-gray-600 flex gap-2">
        <p>Data: {result.date}</p>
        <p>Ano: {result.year}</p>
        <p>Edição: {result.edition}</p>
      </section>
      <p
        className="text-sm text-black mt-2"
        dangerouslySetInnerHTML={{ __html: highlightedSnippet }}
      />
    </article>
  );
};

export default SearchResultItem;
