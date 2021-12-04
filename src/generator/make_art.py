""" A script that makes unicode art out of images. Used to make unicode art of
chara sprites for printing out to the terminal

Author: Phoney Badger (https://gitlab.com/phoneybadger)
(c) 08-08-2021
Modified: Juan Louis R (https://github.com/mizuday)
(c) 02-12-2021


Usage:
-run the shell script that downloads all the chara images
-adjust the paths in the main function of this script
-run the script. It should output the correct color files
"""
import skimage.io as io
import numpy as np
import skimage.transform as tm
import os

path_to_charalist = 'charalist.txt' 
path_to_images = 'images/original' 
output_path = 'colorscripts'         


def main():
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for file in os.listdir(path_to_images):
        chara = os.fsdecode(file)
        print(chara)
        if chara.endswith(".png"):
            chara = chara.strip(".png")
            try:
                chara_art = get_chara_art(chara,path_to_images,with_resize=True)
            except Exception as e:
                # raise Exception()
                print(f"couldn't generate art for {chara}")
                print(e)
                continue
            # print(chara_art)
            # remove first 5 lines of character
            # chara = chara[5:]
            write_chara_to_file(chara,chara_art,output_path)

def write_chara_to_file(chara,chara_art,output_path):
    with open(f'{output_path}/{chara}.txt','w') as file:
        file.write(chara_art)

def get_chara_art(chara,path_to_images,with_resize=False):
    """ Takes the name of a chara and prints out its art"""

    # string to hold the color formatted string
    chara_art=''

    # loading in image
    path = f'{path_to_images}/{chara}.png'
    original_image = io.imread(path)
    image_cropped = crop_image_to_content(original_image)
    # whether to scale down images that are too large.leads to loss in quality
    if with_resize:
        height,width,channels = image_cropped.shape
        height_threshold=32
        if height>height_threshold:
            print(f'{chara} too large')
            scale = height / 32
            image_cropped=tm.resize(image_cropped,(int(height/scale),int(width/scale),channels),anti_aliasing=False)
            image_cropped=image_cropped*255
    # doubling on the width axis as characters are not as wide as they are high
    image = np.repeat(image_cropped,2,1)
    image = image.astype(np.uint8)
    rows,columns,_ = image.shape

    # creating matrix for storing the unicode glyphs
    string_matrix = np.full((rows,columns),fill_value=' ',dtype=str)
    # set all non transparent pixels to the block glyph
    string_matrix[image[:,:,3]==255]='█'

    # print out the image with appropriate colors
    for i in range(rows):
        chara_art+='\n'
        old_color=None
        for j in range(columns):
            r,g,b=image[i,j,:3]
            new_color = get_color_escape(r,g,b,background=False)
            if new_color==old_color:
                color_escape=''
            else:
                color_escape=new_color
                old_color=new_color

            chara_art+=f'{color_escape}{string_matrix[i,j]}'
    chara_art+='\033[0m\n'
    return chara_art


def crop_image_to_content(image):
    """Crops the image so that all non essential space is removed"""

    # Finding coordinates for a bounding box of the content
    alpha_channel = image[:,:,3]
    min_x,min_y = find_top_left(alpha_channel)
    cropped_half=image[min_y:,min_x:,:]

    #flip image and perform the same action to crop other corner
    flipped_image = np.flip(cropped_half,(0,1))
    max_x,max_y = find_top_left(flipped_image[:,:,3])
    full_cropped_flipped = flipped_image[max_y:,max_x:,:]

    #flip back to restore original orientation
    cropped_image = np.flip(full_cropped_flipped,(0,1))

    return cropped_image

def find_top_left(alpha_channel):
    """Finds top left corner of bounding box to crop to content and returns
       coordinates of top left"""
    # first non alpha values on each column and row. argmax works as only 0,255
    # values are present
    min_values_x = alpha_channel.argmax(axis=1)
    min_values_y = alpha_channel.argmax(axis=0)
    # top left corner of bounding box
    min_x = np.min(min_values_x[min_values_x!=0])
    min_y = np.min(min_values_y[min_values_y!=0])

    return min_x,min_y

def get_color_escape(r, g, b, background=False):
    """ Given rgb values give the escape sequence for printing out the color"""
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

def update_charalist():
    with open(path_to_charalist, 'w') as charlist:
        for file in os.listdir(output_path):
            chara = os.fsdecode(file)
            print(chara)
            if chara.endswith(".txt"):
                chara = chara.strip(".txt")
                charlist.write(f'{chara}\n')

if __name__=='__main__':
    main()
    update_charalist()
