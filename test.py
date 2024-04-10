from PIL import Image
import pytesseract
import os
from concurrent.futures import ThreadPoolExecutor

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

input_folder = './assets/images/'
image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
output_folder = './assets/txt/'

def process_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang='por')
    output_file_path = os.path.join(output_folder, os.path.splitext(os.path.basename(image_path))[0] + '.txt')
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Text extracted from", os.path.basename(image_path), "and saved to", output_file_path)

def process_all_images(image_files):
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_image, image_files)

image_files = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder) if any(filename.lower().endswith(ext) for ext in image_extensions)]

process_all_images(image_files)
