#!/bin/sh

PATH_TO_NAMES='charalist.txt'
PATH_TO_IMAGES='images/original'

# script to download all images of chara from charadb
while IFS= read -r line; do
  wget -P $PATH_TO_IMAGES 'https://emoji.gg/assets/emoji/'$line'.png'

done < $PATH_TO_NAMES
