from PIL import Image
import csv
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')

def superpose_images(
    image1_path="generated_images/generated_image.png",
    image2_path="assets/images/layer2.png",
    image3_path="assets/images/layer3.png",
    output_path="superposed_image.png",
    opacity=0.7
):
    # Open the three images
    image1 = Image.open(image1_path).convert("RGBA")
    image2 = Image.open(image2_path).convert("RGBA")
    image3 = Image.open(image3_path).convert("RGBA")

    # Ensure all images have the same size
    image2 = image2.resize(image1.size)
    image3 = image3.resize(image1.size)

    # Superpose image1 and image2 at given opacity
    intermediate_image = Image.blend(image1, image2, opacity)

    # Superpose the result with image3 at full opacity
    superposed_image = Image.alpha_composite(intermediate_image, image3)

    # Save the result
    superposed_image.save(output_path)


def load_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=':')
        return list(reader)

def load_fonts_pdj():
    fnt_pensee = ImageFont.truetype("apps/static/assets/fonts/josefin.ttf", 60)
    fnt_auteur = ImageFont.truetype("apps/static/assets/fonts/moontime.ttf", 70)
    return fnt_pensee, fnt_auteur

def load_fonts_pds():
    fnt_pensee = ImageFont.truetype("apps/static/assets/fonts/Alegreya_Sans/AlegreyaSans-Bold.ttf", 80)
    fnt_auteur = ImageFont.truetype("apps/static/assets/fonts/PlaylistFF/PlaylistScript.otf", 70)
    return fnt_pensee, fnt_auteur

def wrap_text(draw, text, font, line_width):
    lines = []
    line = ''
    for word in text.split():
        bbox = draw.textbbox((0, 0), line + word, font=font)
        if bbox[2] - bbox[0] <= line_width:
            line += f' {word}'
        else:
            lines.append(line.lstrip())
            line = word
    if line:
        lines.append(line.lstrip())
    return lines


def draw_text_on_image(img, text, author, fnt_pensee, fnt_auteur):
    draw = ImageDraw.Draw(img)

    # Wrap and draw main text
    lines = wrap_text(draw, text, fnt_pensee, 750)
    bbox = draw.textbbox((0, 0), 'Aj', font=fnt_pensee)
    line_height = bbox[3] - bbox[1]
    y = img.size[1] // 2 - line_height * len(lines) // 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=fnt_pensee)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((img.size[0] - w) // 2, y), line, font=fnt_pensee, fill=(255, 255, 255))
        y += h

    # Draw author name
    author_bbox = draw.textbbox((0, 0), author, font=fnt_auteur)
    author_w = author_bbox[2] - author_bbox[0]
    draw.text(((img.size[0] - author_w) // 2, 770), author, font=fnt_auteur, fill="#f2ea67")


def process_quote(service="Pensée De Saint", author="", text="", fnt_pensee="", fnt_auteur="", filepath="generated.png"):
    if service is not None:
        if service == "Pensée De Saint":
            template_path = "apps/static/assets/img/vds/superposed_image_pds.png"
        elif service == "Pensée Du Jour":
            template_path = "apps/static/assets/img/vds/superposed_image_pdj.png"

    img = Image.open(template_path)
    draw_text_on_image(img, text, author, fnt_pensee, fnt_auteur)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath, "PNG", quality=100, optimize=True)
    #img.show()
