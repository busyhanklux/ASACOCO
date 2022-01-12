import torch  # FB之深度學習框架
import cv2
import numpy as np

url="http://192.168.43.211:81/stream"

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
# print(model)
# img=cv2.imread('IMG_2997.JPG')

img = cv2.VideoCapture(url)

results = model(img)
results.print()
print(results.xyxy)  # xy軸座標，xy軸的長寬
cv2.imshow('YOLO COCO', np.squeeze(results.render()))
cv2.waitKey(0)
