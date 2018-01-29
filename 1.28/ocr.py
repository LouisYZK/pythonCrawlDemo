from PIL import Image
import pytesseract
image = Image.open('code2.png')
image = image.convert('L')
box =(5,9,71,19)
image = image.crop(box)
# image.save('new.png')
x = image.size[0]*3
y = image.size[1]*3
image = image.resize((x,y))
code = pytesseract.image_to_string(image)
print(code)
box =(66,34,111,48)
im2 =  Image.open('code2.png').crop(box)
im2 = im2.convert('L')
x = im2.size[0]*6
y = im2.size[1]*6
im2 = im2.resize((x,y))
code2 = pytesseract.image_to_string(im2)
print(code2)