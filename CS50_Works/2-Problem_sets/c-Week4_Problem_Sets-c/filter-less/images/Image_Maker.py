from cs50 import get_string
from cs50 import get_int
from PIL import Image , ImageFilter


Process_Image = input("Write the image path that you want to Work with : \n")
Process_Type = get_int("What type of process that you want ? \n 1:Flip Image Horizontally \n 2:Flip Image Vertically \n 3:Blur Image \n 4:Negative Image \n 5:Sepia Image \n 6:Grey Image \n")
Before_Image = Image.open(f"{Process_Image}.bmp")
New_Image_Name = get_string("Enter the new file name : \n")


if Process_Type == 1:
    After = Before_Image.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
    After.save(f"{New_Image_Name}.bmp")

elif Process_Type ==2:
    After = Before_Image.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
    After.save(f"{New_Image_Name}.bmp")

elif Process_Type ==3:
    After = Before_Image.filter(filter=ImageFilter.BLUR)
    After.save(f"{New_Image_Name}.bmp")

elif Process_Type ==5:
    After = Before_Image.filter(filter=ImageFilter.BLUR)
    After.save(f"{New_Image_Name}.bmp")