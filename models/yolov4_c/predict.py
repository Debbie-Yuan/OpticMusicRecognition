from PIL import Image

from yolo import YOLO

yolo = YOLO()
img = input('Input image filename:')
image = Image.open(img)
image = image.convert('RGB')
r_image, ob, os, oc = yolo.detect_image(image)

r_image.show()

# while True:
#     img = input('Input image filename:')
#     if img == "exit":
#         break
#     try:
#         image = Image.open(img)
#         image = image.convert('RGB')
#     except:
#         print('Open Error! Try again!')
#         continue
#     else:
#         # top, left, bottom, right = out_boxes[0]
#         # nimg = image_crop(image, left, top, right, bottom)
#         # out_boxes, out_scores, out_classes = yolo.predict(image)
#         r_image, ob, os, oc = yolo.detect_image(image)
#         r_image.show()
#
#
#
#         # nimg.show()
