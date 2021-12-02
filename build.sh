#!/bin/sh
./scripts/generate_charlist.sh
./scripts/scrape.sh
# ./scripts/downscale_images.sh
./scripts/generate_art.sh