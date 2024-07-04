import os
import shlex
import json
import fitz
import pytesseract
import io
import click
import shutil
from pathlib import Path
from tqdm import tqdm
from PIL import Image
from loguru import logger

# Configuração do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"


def get_tessdata_path():
    """Obtém o caminho do diretório tessdata."""
    return Path().resolve() / "tessdata"


def extract_text_from_image(image, config_flags):
    """Extrai texto de uma imagem usando OCR."""
    return pytesseract.image_to_string(image, lang="por", config=config_flags)


def process_pdf(pdf_path, images_dir, config_flags):
    """Processa um arquivo PDF e extrai texto."""
    doc = fitz.open(pdf_path)
    pdf_name = os.path.basename(pdf_path)
    pages_text = []

    for page_num in tqdm(range(len(doc)), desc=f"Extracting text from {pdf_name}"):
        page = doc.load_page(page_num)
        text = page.get_text()

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            image_path = os.path.join(
                images_dir, f"{pdf_name[:-4]}_p{page_num+1}_img{img_index+1}.png"
            )
            image.save(image_path)
            text += "\n" + extract_text_from_image(image, config_flags)

        pages_text.append({"number": page_num + 1, "text": text})

    return pages_text


def update_json(json_path, pdf_path, pages_text):
    """Atualiza o arquivo JSON com o texto extraído das páginas."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    pdf_entry = next(
        (entry for entry in data["pdf_links"].values() if entry["path"] == pdf_path),
        None,
    )
    if pdf_entry:
        pdf_entry["pages"] = pages_text

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


@click.command()
@click.argument("workdir", type=click.Path(exists=True))
def extract_cli(workdir):
    """Extrai texto de arquivos PDF em um diretório."""
    tessdata_path = get_tessdata_path()
    config_flags = rf"--tessdata-dir {shlex.quote(str(tessdata_path))}"

    workdir_path = Path(workdir).resolve()
    pdf_dir = workdir_path / "pdf"
    images_dir = workdir_path / "images"
    json_path = workdir_path / "data.json"
    output_dir = workdir_path / "txt"

    if not images_dir.exists():
        os.makedirs(images_dir)
    if not output_dir.exists():
        os.makedirs(output_dir)

    for each_path in os.listdir(pdf_dir):
        if each_path.endswith(".pdf"):
            pdf_path = pdf_dir / each_path
            pages_text = process_pdf(pdf_path, images_dir, config_flags)
            update_json(json_path, str(pdf_path), pages_text)

    shutil.rmtree(images_dir)
    logger.success("Done!")


if __name__ == "__main__":
    extract_cli()
