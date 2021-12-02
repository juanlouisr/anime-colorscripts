import cv2
import os

def downscale(source, dest):
    im = cv2.imread(source, cv2.IMREAD_UNCHANGED)
    if im is None:
        print(f"Cant read {source}")
    else:
        imResized = cv2.resize(im, (32, 32))            
        cv2.imwrite(dest, imResized)

def main():
    image_source = "images/original/"
    image_dest   = "images/downscaled/"

    if not os.path.exists(image_dest):
        os.makedirs(image_dest)

    directory = os.fsencode(image_source)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        print(filename)
        if filename.endswith(".png"):
            downscale(f"{image_source}{filename}", 
            f"{image_dest}{filename}")

if __name__=="__main__":
    main()