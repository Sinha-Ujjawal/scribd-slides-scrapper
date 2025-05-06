#!/usr/bin/python3
import argparse
import os
import logging
import re
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_EXCEPTION

import requests
from bs4 import BeautifulSoup

IMAGE_FORMAT = ".webp"  # extension to use to save the downloaded image files

def download_slides(url, out, max_workers):
    out = os.path.abspath(out)
    logging.info(f"Ensuring directory: {out} exists")
    os.makedirs(out, exist_ok=True)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    logging.info(f"Calling GET on url: `{url}`")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error occurred while calling GET on url: `{url}`: {response.text}")
    soup = BeautifulSoup(response.text, "html.parser")
    slide_images = soup.find_all("img", id=re.compile("^slide-image-\d+"))
    logging.info(f"Total slides to download: {len(slide_images)}")

    def download_slide(slide_image):
        # srcset format:
        # https://image.slidesharecdn.com/rchprogramme-200717085035/85/Rch-programme-1-320.jpg 320w, https://image.slidesharecdn.com/rchprogramme-200717085035/85/Rch-programme-1-638.jpg 638w, https://image.slidesharecdn.com/rchprogramme-200717085035/75/Rch-programme-1-2048.jpg 2048w
        src, _ = slide_image["srcset"].split(", ")[-1].split(" ")  # Taking the largest image from the srcset
        dst = os.path.join(out, slide_image["id"] + IMAGE_FORMAT)
        logging.info(f"Downloading image from `{src}` and saving to `{dst}`")
        img_content = requests.get(src).content
        with open(dst, "wb") as fp:
            fp.write(img_content)
        logging.info(f"Downloaded image from `{src}` and saving to `{dst}`")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        wait((executor.submit(download_slide, slide_image) for slide_image in slide_images),
             return_when=FIRST_EXCEPTION)
    logging.info(f"Downloaded all slides from `{url}` to `{out}`")

def main():
    parser = argparse.ArgumentParser("Helper script to download slide images from scribd")
    parser.add_argument(
        "--url",
        required=True,
        help="Scribd slides preview url (e.g.- https://www.slideshare.net/JavedSheikh20/rch-programme-236992429#1)",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Path of the folder where to store the downloaded slides as .webp images",
    )
    parser.add_argument(
        "--max-workers",
        required=False,
        type=int,
        default=4,
        help="Max. no of workers to use for multithreading",
    )
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    args = parser.parse_args()
    download_slides(args.url, args.out, args.max_workers)

if __name__ == "__main__":
    main()
