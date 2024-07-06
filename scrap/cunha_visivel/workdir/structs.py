from datetime import datetime
import os
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field


URL = str


class PDFPage(BaseModel):
    number: int
    text: str


class PDFInformation(BaseModel):
    hash_sha512: str
    path: Path
    pages: list[PDFPage]


class CunhaVisivelDB(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    pdf_links: dict[URL, PDFInformation] = {}

    def try_add_pdf_link(self, url: URL, pdf_information: PDFInformation):
        if url in self.pdf_links:
            return False
        self.pdf_links[url] = pdf_information
        self.updated_at = datetime.now()
        return True

    def try_add_page(self, path: Path, pdf_page: PDFPage):
        path_str = "pdf/" + str(path)
        for diario in self.pdf_links.values():
            if str(diario.path) == path_str:
                for page in diario.pages:
                    if not isinstance(pdf_page, PDFPage):
                        pdf_page = PDFPage(**pdf_page)
                    if not isinstance(page, PDFPage):
                        page = PDFPage(**page)
                    if isinstance(page, PDFPage) and page.number == pdf_page.number:
                        return None
                diario.pages.append(pdf_page)
                self.updated_at = datetime.now()
                return True
        return False

    def page_exists(self, path: Path, total_pages: int):
        path_str = "pdf/" + str(path)
        for diario in self.pdf_links.values():
            if str(diario.path) in path_str and total_pages == len(diario.pages):
                return True
        return False

    def log_empty_pages(self) -> List[URL]:
        urls = []
        for diario in self.pdf_links.values():

            if len(diario.pages) == 0:
                urls.append(diario.path)

        return urls
