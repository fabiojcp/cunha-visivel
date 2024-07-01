from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field


URL = str


class PDFInformation(BaseModel):
    hash_sha512: str
    path: Path


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
