import { Analytics } from '@vercel/analytics/react';

import { Inter } from "next/font/google";
import "@/styles/globals.css";
import "@/styles/reset.css";
import Head from "next/head";

const metadata = {
  title: "Cunha visivel",
  description:
    "Cunha visivel é um projeto de transparência e fiscalização da Câmara Municipal e da Prefeitura de Cunha/SP. Através de dados abertos, buscamos facilitar o acesso à informação e promover a participação cidadã. Os diários oficiais de Cunha não são indexáveis, pois são imagens, e não texto, transformamos os arquivos de imagem que contenham texto para arquivo de texto, para serem indexados.",
};

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  title = metadata.title,
  description = metadata.description,
  children,
}: Readonly<{
  title?: string;
  description?: string;
  children: React.ReactNode;
}>) {
  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="description" content={description} />
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
      </Head>
      <div className={`${inter.className} w-full min-h-screen flex flex-col`}>
        {children}
      </div>
      <Analytics />
    </>
  );
}
