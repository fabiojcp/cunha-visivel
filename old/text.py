from PIL import Image
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

input_folder = "./assets/images/"
image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]
output_folder = "./assets/txt/"

for filename in os.listdir(input_folder):
    if any(filename.lower().endswith(ext) for ext in image_extensions):

        image_path = os.path.join(input_folder, filename)

        img = Image.open(image_path)

        text = pytesseract.image_to_string(img, lang="por")

        output_file_path = os.path.join(
            output_folder, os.path.splitext(filename)[0] + ".txt"
        )
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(text)

        print("Text extracted from", filename, "and saved to", output_file_path)
