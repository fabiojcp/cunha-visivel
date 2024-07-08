"use client";

import Image from "next/image";
import { useState } from "react";
import { MdArrowDropUp, MdArrowDropDown } from "react-icons/md";

import Logo from "@/assets/logo.png";
import Filter from "@/components/filters";
import SearchInput from "@/components/search-input";

interface SearchTopProps {
  currentPage: number;
  totalPages: number;
  totalResults: number;
}

const SearchTop: React.FC<SearchTopProps> = ({
  currentPage,
  totalPages,
  totalResults,
}) => {

  const [isResultsPerPageOpen, setIsResultsPerPageOpen] = useState(false);
  const [isSortOrderOpen, setIsSortOrderOpen] = useState(false);
  const [isShowDuplicatesOpen, setIsShowDuplicatesOpen] = useState(false);

  return (
    <>
      <section className="w-full flex pl-2 py-4 justify-start items-center gap-4">
        <Image
          src={Logo}
          width={92}
          height={92}
          alt="Logotipo da Cunha em um círculo vermelho com o texto 'Cunha' em branco e um contorno de montanha no fundo"
        />
        <article className="py-4 w-full">
          <SearchInput />
        </article>
      </section>
      <section className="mb-4 pl-10">
        <p className="text-gray-700">
          Mostrando página {currentPage} de {totalPages} páginas, total de
          resultados: {totalResults}
        </p>
      </section>
      <section className="mb-4 pl-10"></section>
      <hr className="w-full h-[1px] bg-black opacity-60" />
      <section className="pt-4 pb-2 flex gap-6 pl-10">
        <Filter
          title="Resultados por página"
          isOpen={isResultsPerPageOpen}
          setIsOpen={setIsResultsPerPageOpen}
          options={[
            { label: "10 por página", value: "10" },
            { label: "50 por página", value: "50" },
            { label: "100 por página", value: "100" },
          ]}
          query={"r"}
          defaultValue="100"
        />
        <Filter
          title="Ordem"
          isOpen={isSortOrderOpen}
          setIsOpen={setIsSortOrderOpen}
          options={[
            { label: "Mais antigo para novo", value: "ASC" },
            { label: "Mais novo para mais antigo", value: "DESC" },
          ]}
          query={"s"}
          defaultValue="DESC"
        />

        <Filter
          title="Mostrar duplicados"
          isOpen={isShowDuplicatesOpen}
          setIsOpen={setIsShowDuplicatesOpen}
          options={[
            { label: "Mostrar arquivos repetidos", value: "t" },
            { label: "Não mostrar arquivos repetidos", value: "f" },
          ]}
          query={"d"}
          defaultValue={"t"}
        />
      </section>
    </>
  );
};

export default SearchTop;
