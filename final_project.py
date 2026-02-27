import os
from PIL import Image  

path = "/home/student/supplier-data/images"

for x in os.listdir(path):
    if x.endswith(".TIFF"):  # only process TIFF files
        imgPath = os.path.join(path, x)
        img = Image.open(imgPath)
        img = img.convert("RGB")   # convert RGBA → RGB
        newimg = img.resize((600, 400))  # resize
        # save with same name but JPEG extension
        new_filename = os.path.splitext(x)[0] + ".jpeg"
        newimg.save(os.path.join(path, new_filename), format="JPEG")