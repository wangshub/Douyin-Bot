from PIL import Image

im = Image.open("../autojump.png")
w, h = im.size

area = (0, 0, 50, 50)

im_croped = im.crop(area)

im_croped.show()
