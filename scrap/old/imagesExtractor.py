import os
from pathlib import Path
import shlex
import fitz
import pytesseract
import io
from tqdm import tqdm
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

FILE_PATH = Path(__file__).resolve().parent

TESSDATA_PATH = FILE_PATH / "tessdata"

workdir = "./assets/pdf"
output_dir = "./assets/txt/"

tesseract_config_flags = rf"--tessdata-dir {shlex.quote(str(TESSDATA_PATH))}"


def extract_text_from_image(image):
    text = pytesseract.image_to_string(image, lang="por", config=tesseract_config_flags)
    return text


for each_path in os.listdir(workdir):
    if each_path.endswith(".pdf"):
        doc = fitz.open(os.path.join(workdir, each_path))

        for page_num in tqdm(range(len(doc)), desc=f"Extracting text from {each_path}"):
            page = doc.load_page(page_num)
            text = page.get_text()

            for img in page.get_images(full=True):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                text += "\n" + extract_text_from_image(image)

            output_file_path = os.path.join(
                output_dir, f"{each_path[:-4]}_page{page_num + 1}.txt"
            )
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(text)

print("Done!")
