import { Inter } from "next/font/google";

import type { Metadata } from "next";
import "@/styles/globals.css";
import "@/styles/reset.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Cunha visivel",
  description:
    "Cunha visivel é um projeto de transparência e fiscalização da Câmara Municipal e da Prefeitura de Cunha/SP. Através de dados abertos, buscamos facilitar o acesso à informação e promover a participação cidadã. Os diários oficiais de Cunha não são indexáveis, pois são imagens, e não texto, transformamos os arquivos de imagem que contenham texto para arquivo de texto, para serem indexados.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <link rel="shortcut icon" href="/images/favicon.ico" />
      <link
        rel="apple-touch-icon"
        sizes="180x180"
        href="/images/favicon.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="32x32"
        href="/images/favicon.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="16x16"
        href="/images/favicon.png"
      />
      <body className={`${inter.className} w-full min-h-screen flex flex-col`}>
        {children}
      </body>
    </html>
  );
}
