from PIL import Image

Before = Image.open(r"filter-less\images\Courtyard.bmp",'r')
After = Before.transpose(method=Before.Transpose.FLIP_LEFT_RIGHT)
After.save("Newimage.bmp")