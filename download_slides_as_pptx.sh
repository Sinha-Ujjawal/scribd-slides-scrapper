#!/bin/bash

set -xe

if [[ -z "$PYTHON_EXEC" ]]; then
    PYTHON_EXEC=python3
fi

usage() {
    echo "Usage: $0 <url> <out> [scale: (default 0.5)] [workers: (default 4 )]"
}

if [[ "$1" == "help" ]]; then
    usage
    exit 0
fi

url="$1"
out="$2"
scale=$3
max_workers=$4

if [[ -z "$max_workers" ]]; then
    max_workers=4
fi

if [[ -z "$scale" ]]; then
    scale=0.5
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -z "$url" ]]; then
    echo "<url> not provided!"
    usage
    exit 1
fi

if [[ -z "$out" ]]; then
    echo "<out> not provided!"
    usage
    exit 1
fi

tempdir=$(mktemp -d)
$PYTHON_EXEC $SCRIPT_DIR/download_slides_as_images.py --url "$url" --out "$tempdir" --max-workers $max_workers
find $tempdir -type f -name "*.webp" | \
    sort -t '-' -k 3 -n | \
    xargs $PYTHON_EXEC $SCRIPT_DIR/images_to_pptx.py --out "$out" --scale $scale --max-workers $max_workers --image-paths
rm -rf $tempdir
