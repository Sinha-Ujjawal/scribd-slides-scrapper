# Helper python/shell scripts to download slides from [slideshare](https://www.slideshare.net/)
This repository contains python/shell helper scripts to download slides from [slideshare](https://www.slideshare.net/) as [webp](https://en.wikipedia.org/wiki/WebP) images and save it as a [pptx](https://en.wikipedia.org/wiki/Microsoft_PowerPoint) file.

## Getting Started

1. Download a latest version of [`python >= 3.10`](https://www.python.org/)

2. Install all requirements from [requirements.txt](./requirements.txt) file

```console
> python3 -m pip install -r requirements.txt
```

## Usage

1. [download_slides_as_images.py](./download_slides_as_images.py)

This is a python script that downloads the slides from slideshare url as .webp files

```console
> python3 download_slides_as_images.py --help
usage: Helper script to download slide images from scribd [-h] --url URL --out OUT [--max-workers MAX_WORKERS]

options:
  -h, --help            show this help message and exit
  --url URL             Scribd slides preview url (e.g.- https://www.slideshare.net/JavedSheikh20/rch-programme-236992429#1)
  --out OUT             Path of the folder where to store the downloaded slides as .webp images
  --max-workers MAX_WORKERS
                        Max. no of workers to use for multithreading
```

2. [images_to_pptx.py](./images_to_pptx.py)

This is a python script that can converts a list of images to a ppt file

```console
> python3 images_to_pptx.py --help
usage: images_to_pptx.py [-h] --out OUT --image-paths IMAGE_PATHS [IMAGE_PATHS ...]

options:
  -h, --help            show this help message and exit
  --out OUT             Path of the pptx output
  --image-paths IMAGE_PATHS [IMAGE_PATHS ...]
                        List of image paths
```

3. [download_slides_as_pptx.sh](./download_slides_as_pptx.sh)

This is a helper shell script that uses above two scripts to download the slides from given url and convert that to .ppt file

```console
> sh download_slides_as_pptx.sh help
Usage: download_slides_as_pptx.sh <url> <out> [workers: (default 4)]
```

## Copyright

Licensed under [@MIT](./LICENSE)

