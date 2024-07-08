"use client";

import { useState } from "react";

import { useQueryHandler } from "../hook/useQueryHandler";

export default function SearchInput() {
  const { searchParams, createQueryString } = useQueryHandler();

  const search = searchParams?.get("q");

  const [query, setQuery] = useState(search || "");

  function handleSubmit(
    e: React.FormEvent<HTMLFormElement> | React.MouseEvent<HTMLButtonElement>
  ) {
    e.preventDefault();
    if (query) {
      createQueryString("q", query, "search");
    }
  }

  return (
    <form
      className="flex w-full max-w-[500px] bg-white border border-solid border-black rounded-full px-4 py-2"
      onSubmit={(e: React.FormEvent<HTMLFormElement>) => {
        handleSubmit(e);
      }}
    >
      <input
        placeholder="Pesquise em Cunha visível"
        className="border-none rounded-full w-[calc(100%-1.25rem)] bg-white text-black outline-none focus:outline-none focus-visible:outline-none"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button
        className="w-5 h-full flex justify-center items-center"
        type="submit"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          fill="none"
          viewBox="0 0 16 16"
          className="w-full h-full opacity-30"
        >
          <g clipPath="url(#a)">
            <path
              fill="#000"
              d="M14 12.94 10.16 9.1c1.25-1.76 1.1-4.2-.48-5.78a4.49 4.49 0 0 0-6.36 0 4.49 4.49 0 0 0 0 6.36 4.486 4.486 0 0 0 5.78.48L12.94 14 14 12.94ZM4.38 8.62a3 3 0 0 1 0-4.24 3 3 0 0 1 4.24 0 3 3 0 0 1 0 4.24 3 3 0 0 1-4.24 0Z"
            />
          </g>
          <defs>
            <clipPath id="a">
              <path fill="#fff" d="M0 0h16v16H0z" />
            </clipPath>
          </defs>
        </svg>
      </button>
    </form>
  );
}
