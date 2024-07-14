import os
import shlex
import json
import PyPDF2
import pytesseract
import click
import shutil
from pathlib import Path
from tqdm import tqdm
from PIL import Image
from pdf2image import convert_from_path
from loguru import logger

from cunha_visivel.workdir.structs import CunhaVisivelDB

# Verifies if Tesseract is installed and sets the path
if shutil.which("tesseract") is None:
    raise EnvironmentError("Tesseract OCR is not installed or not in the system PATH.")

# Tesseract configuration
pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract")


def get_tessdata_path():
    # Gets the path to the tessdata directory.
    return Path().resolve() / "tessdata"


def extract_text_from_image(image, config_flags):
    # Extracts text from an image using OCR.
    return pytesseract.image_to_string(image, lang="por", config=config_flags)


def process_pdf(pdf_path, images_dir, config_flags, db: CunhaVisivelDB):
    # Processes a PDF file and extracts text.
    pdf_name = os.path.basename(pdf_path)
    pages_text = []

    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        total_pages = len(reader.pages)

        # Checks if all pages have already been processed
        all_pages_processed = db.page_exists(pdf_path, total_pages)
        if all_pages_processed:
            logger.info(f"All pages of {pdf_name} already processed, skipping...")
            return pages_text

    logger.info(f"Processing {pdf_name}...")

    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page_num in tqdm(
            range(total_pages), desc=f"Extracting text from {pdf_name}"
        ):
            if db.page_exists(pdf_path, page_num + 1):
                logger.info(
                    f"Page {page_num + 1} of {pdf_name} already processed, skipping..."
                )
                continue

            page = reader.pages[page_num]
            text = page.extract_text()

            # Converts the PDF page to an image
            images = convert_from_path(
                pdf_path, first_page=page_num + 1, last_page=page_num + 1
            )
            for img_index, image in enumerate(images):
                image_path = os.path.join(
                    images_dir, f"{pdf_name[:-4]}_p{page_num+1}_img{img_index+1}.png"
                )
                image.save(image_path)
                text += "\n" + extract_text_from_image(image, config_flags)

            pages_text.append({"number": page_num + 1, "text": text})

    return pages_text


def update_json(
    json_path: Path, pdf_path: Path, pages_text: str, db: CunhaVisivelDB
) -> None:
    pdf_name = os.path.basename(pdf_path)
    for page in pages_text:
        try_add_page = CunhaVisivelDB.try_add_page(db, pdf_name, page)
        if try_add_page:
            logger.info(f"Added page {pdf_name} to the database.")
            json_path.write_text(db.model_dump_json(indent=2))
            continue
        if try_add_page is None:
            logger.warning(
                f"Page {pdf_name} already exists in the database, skipping..."
            )
            continue
        logger.error(f"Failed to add page {pdf_name} to the database.")


@click.command()
@click.argument("workdir", type=click.Path())
@click.option(
    "--limit",
    default=None,
    type=int,
    help="Limits the number of files to be processed.",
)
@click.option(
    "--empty-pages",
    is_flag=True,
    help="Log URLs of PDF links that do not have any pages.",
)
def extract_cli(workdir: str, limit: int | None, empty_pages: bool) -> None:
    # Extracts text from PDF files in a directory.
    workdir_path = Path(workdir).absolute()

    if ".workdir" not in workdir_path.suffix:
        workdir_path = Path(str(workdir_path) + ".workdir").absolute()

    if not workdir_path.exists():
        logger.error(f"Directory {workdir_path} does not exist.")
        return

    pdf_dir = workdir_path / "pdf"
    images_dir = workdir_path / "images"
    json_path = workdir_path / "db.json"

    db = CunhaVisivelDB.model_validate_json(json_path.read_text())

    if empty_pages:
        empty_urls = db.log_empty_pages()

        if empty_urls:
            for url in empty_urls:
                logger.info(f"PDF link {url} has no pages.")
            logger.info(f"A total of {len(empty_urls)} PDFs have no pages.")
        else:
            logger.success("All PDFs have pages.")

        return

    if not images_dir.exists():
        os.makedirs(images_dir)

    logger.info(f"Extracting text from PDFs in {workdir_path.suffix}...")

    tessdata_path = get_tessdata_path()
    config_flags = rf"--tessdata-dir {shlex.quote(str(tessdata_path))}"

    reached_limit = 0
    count = 0
    for each_path in os.listdir(pdf_dir):
        if each_path.endswith(".pdf"):
            if reached_limit == limit:
                break
            pdf_path = pdf_dir / each_path
            pages_text = process_pdf(pdf_path, images_dir, config_flags, db)
            update_json(json_path, str(pdf_path), pages_text, db)
            reached_limit += 1
            count += 1

    shutil.rmtree(images_dir)
    logger.success(f"Total of {count} processed. Done!")


if __name__ == "__main__":
    extract_cli()