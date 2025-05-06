#!/usr/bin/python3
import os
import argparse
import logging
from glob import glob
import tempfile

from pptx import Presentation
from pptx.util import Inches, Pt
from PIL import Image

TEMP_FILES = []

def convert_if_webp(image_path):
    if image_path.lower().endswith(".webp"):
        with Image.open(image_path) as img:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            logging.info(f"Saving {image_path} to {temp_file.name}")
            img.save(temp_file.name, "PNG")
            TEMP_FILES.append(temp_file.name)
            return temp_file.name
    return image_path

def convert_images_to_pptx(image_paths, out):
    out = os.path.abspath(out)
    prs = Presentation()
    slide_width = prs.slide_width
    slide_height = prs.slide_height
    blank_layout = prs.slide_layouts[6]  # blank layout
    for img_path in image_paths:
        img_path = os.path.abspath(img_path)
        logging.info(f"Adding slide for image: {img_path}")
        slide = prs.slides.add_slide(blank_layout)
        with Image.open(img_path) as img:
            img_width_px, img_height_px = img.size
            img_dpi = img.info.get("dpi", (96, 96))
            img_width_in = img_width_px / img_dpi[0]
            img_height_in = img_height_px / img_dpi[1]
        # Convert to pptx units (EMU)
        img_width = Inches(img_width_in)
        img_height = Inches(img_height_in)
        # Scale to fit slide while maintaining aspect ratio
        scale = min(slide_width / img_width, slide_height / img_height)
        final_width = int(img_width * scale)
        final_height = int(img_height * scale)
        # Center image on slide
        left = int((slide_width - final_width) / 2)
        top = int((slide_height - final_height) / 2)
        slide.shapes.add_picture(convert_if_webp(img_path), left, top, width=final_width, height=final_height)
        logging.info(f"Added slide for image: {img_path}")
    logging.info(f"Saving presentation to {out}")
    prs.save(out)
    logging.info(f"Saved presentation to {out}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        required=True,
        help="Path of the pptx output",
    )
    parser.add_argument(
        "--image-paths",
        nargs="+",
        required=True,
        help="List of image paths",
    )
    args = parser.parse_args()
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    convert_images_to_pptx(args.image_paths, args.out)
    for temp_file in TEMP_FILES:
        logging.info(f"Removing temp file: {temp_file}")
        os.remove(temp_file)
        logging.info(f"Removed temp file: {temp_file}")

if __name__ == "__main__":
    main()
