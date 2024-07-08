import { GiCheckMark } from "react-icons/gi";
import { MdArrowDropDown, MdArrowDropUp } from "react-icons/md";

import { useQueryHandler } from "@/hook/useQueryHandler";

export default function Filter({
  isOpen,
  setIsOpen,
  title,
  options,
  query,
  defaultValue,
}: {
  isOpen: boolean;
  setIsOpen: (value: boolean) => void;
  title: string;
  options: { label: string; value: string }[];
  query: string;
  defaultValue: string;
}) {
  const { searchParams, createQueryString } = useQueryHandler();

  const useFindQuery = (key: string) => {
    const search = searchParams?.get(key);
    return search;
  };

  const queryValue = useFindQuery(query);

  function handleClick(value: string) {
    createQueryString(query, value, "search");
    setIsOpen(false);
  }
  const findTitle = options.find((value) => value.value == queryValue);

  return (
    <div className="relative min-w-[300px]">
      <label
        className="block text-gray-700 mb-2 flex"
        onClick={() => setIsOpen(!isOpen)}
      >
        {findTitle ? findTitle.label : title}
        <span>{isOpen ? <MdArrowDropUp /> : <MdArrowDropDown />}</span>
      </label>
      {isOpen && (
        <div className="absolute mt-1 w-full border border-gray-300 bg-white rounded shadow-lg z-10">
          {options.map((value, index) => (
            <div
              key={value.label + index}
              className="flex gap-2 p-2 hover:bg-gray-200 cursor-pointer text-black"
              onClick={() => handleClick(value.value)}
            >
              {((query && queryValue && queryValue == value.value) ||
                (!query && defaultValue == value.value)) && <GiCheckMark />}
              {value.label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
