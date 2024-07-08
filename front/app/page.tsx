import SearchInput from "@/components/search-input";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center">
      <section className="w-full flex justify-center max-w-[400px] mx-auto">
        <SearchInput />
      </section>
    </main>
  );
}
