import SearchInput from "@/components/search-input";
import { Suspense } from "react";

export default function Home() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <main className="flex min-h-screen flex-col items-center justify-center">
        <section className="w-full flex justify-center max-w-[400px] mx-auto">
          <SearchInput />
        </section>
      </main>
    </Suspense>
  );
}
