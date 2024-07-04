import os
import shlex
import json
import PyPDF2
import pytesseract
import io
import click
import shutil
from pathlib import Path
from tqdm import tqdm
from PIL import Image
from pdf2image import convert_from_path
from loguru import logger

from cunha_visivel.workdir.structs import CunhaVisivelDB

# Verifica se o Tesseract está instalado e define o caminho
if shutil.which("tesseract") is None:
    raise EnvironmentError(
        "Tesseract OCR não está instalado ou não está no PATH do sistema."
    )

# Configuração do Tesseract
pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract")


def get_tessdata_path():
    """Obtém o caminho do diretório tessdata."""
    return Path().resolve() / "tessdata"


def extract_text_from_image(image, config_flags):
    """Extrai texto de uma imagem usando OCR."""
    return pytesseract.image_to_string(image, lang="por", config=config_flags)


def process_pdf(pdf_path, images_dir, config_flags):
    """Processa um arquivo PDF e extrai texto."""
    pdf_name = os.path.basename(pdf_path)
    pages_text = []

    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page_num in tqdm(
            range(len(reader.pages)), desc=f"Extracting text from {pdf_name}"
        ):
            page = reader.pages[page_num]
            text = page.extract_text()

            # Converte a página do PDF para imagem
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


def update_json(json_path: Path, pdf_path: Path, pages_text: str) -> None:
    db = CunhaVisivelDB.model_validate_json(json_path.read_text())
    
    pdf_name = os.path.basename(pdf_path)
    for page in pages_text:
        # print('-------------page----------------')
        # print(page)
        # print("\n")
        # print('\n')
        try_add_page = CunhaVisivelDB.try_add_page(db, pdf_name, page)
        if try_add_page:
            logger.info(f"Added page {pdf_name} to the database.")
            json_path.write_text(db.model_dump_json(indent=2))
            continue
        if try_add_page is None:
            logger.warning(f"Page {pdf_name} already exists in the database, skipping...")
            continue
        logger.error(f"Failed to add page {pdf_name} to the database.")



@click.command()
@click.argument("workdir", type=click.Path())
@click.option(
    "--limit",
    default=None,
    type=int,
    help="Limita a quantidade de arquivos a serem processados.",
)
def extract_cli(workdir, limit):
    # Extrai texto de arquivos PDF em um diretório.
    workdir_path = Path(workdir).absolute()
    logger.info(f"Extracting text from PDFs in {workdir_path.suffix}...")

    if ".workdir" not in workdir_path.suffix:
        workdir_path = Path(str(workdir_path) + ".workdir").absolute()

    if not workdir_path.exists():
        logger.error(f"Directory {workdir_path} does not exist.")
        return

    pdf_dir = workdir_path / "pdf"
    images_dir = workdir_path / "images"
    json_path = workdir_path / "db.json"

    if not images_dir.exists():
        os.makedirs(images_dir)

    tessdata_path = get_tessdata_path()
    config_flags = rf"--tessdata-dir {shlex.quote(str(tessdata_path))}"

    reached_limit = 0
    for each_path in os.listdir(pdf_dir):
        if each_path.endswith(".pdf"):
            if reached_limit == limit:
                break
            pdf_path = pdf_dir / each_path
            pages_text = process_pdf(pdf_path, images_dir, config_flags)
            update_json(json_path, str(pdf_path), pages_text)
            reached_limit += 1

    shutil.rmtree(images_dir)
    logger.success("Done!")


if __name__ == "__main__":
    extract_cli()
