import hashlib
from pathlib import Path
import re

from loguru import logger
import requests

from cunha_visivel.workdir.structs import CunhaVisivelDB, PDFInformation


class WorkdirOperator:
    def __init__(self, workdir_path: Path):
        self.workdir_path = workdir_path
        self.db_path = workdir_path / "db.json"
        self.pdf_dir = workdir_path / "pdf"

        if not self.__isvalid():
            raise FileNotFoundError("Workdir does not exist or is missing files")

        self.db = CunhaVisivelDB.model_validate_json(self.db_path.read_text())

    def __isvalid(self):
        return (
            self.workdir_path.exists()
            and self.db_path.exists()
            and self.pdf_dir.exists()
        )

    def __contains__(self, url: str):
        return url in self.db.pdf_links

    def download_pdf(self, url: str) -> None:
        logger.info(f"Downloading PDF from {url}...")
        pdf_response = requests.get(url)
        logger.info(f"Downloaded PDF from {url}.")

        # Extract filename from pdf_response:
        pdf_filename = re.search(
            r"filename=\"(.*)\"", pdf_response.headers["Content-Disposition"]
        ).groups()[0]
        pdf_path = self.pdf_dir / pdf_filename

        pdf_info = PDFInformation(
            hash_sha512=hashlib.sha512(pdf_response.content).hexdigest(),
            path=pdf_path.relative_to(self.workdir_path),
            pages=[],
        )

        added = self.db.try_add_pdf_link(url, pdf_info)
        if added:
            logger.info(f"Added PDF {url} to the workdir.")
            pdf_path.write_bytes(pdf_response.content)
            logger.info(
                f"Saved PDF to {pdf_path}, size {len(pdf_response.content)} bytes."
            )
            self.commit_db()
            return

        logger.warning(f"PDF {url} already exists in the workdir, skipping...")

    def commit_db(self):
        self.db_path.write_text(self.db.model_dump_json(indent=2))
        logger.info(f"Saved DB to {self.db_path}.")
