import torch
import numpy as np
import cv2

#model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

model = torch.hub.load('ultralytics/yolov5','custom',path='yolov5/runs/train/exp2/weights/best.pt',force_reload=True)

cap = cv2.VideoCapture(0)
#url = "http://192.168.43.211:81/stream"
#cap = cv2.VideoCapture(url)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    frame = cv2.resize(frame, (1024, 768))
    results = model(frame)

    #print(np.array(results.render().shape))
    print(results)  # xy軸座標，xy軸的長寬

    cv2.imshow('YOLO COCO 01', np.squeeze(results.render()))

    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
