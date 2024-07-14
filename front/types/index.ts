export interface Page {
  number: number;
  text: string;
}

export interface PdfLink {
  hash_sha512: string;
  path: string;
  pages: Page[];
  name: string;
  date: string;
  year: string;
  edition: string;
}

export interface Data {
  created_at: string;
  updated_at: string;
  pdf_links: {
    [key: string]: PdfLink;
  };
}

export interface SearchResult {
  page: number;
  snippet: string;
  link: string;
  name: string;
  date: string;
  year: string;
  edition: string;
}

export interface PaginatedResults {
  results: SearchResult[];
  total: number;
  currentPage: number;
  totalPages: number;
}
