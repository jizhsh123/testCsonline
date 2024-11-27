from ultralytics import YOLO
import msilib
import torch
import cv2
model= YOLO('yolov8s.pt')
if __name__ == '__main__':
    # 将模型的训练代码放入这个块中
    result = model.train(data='data.yaml', epochs=5000, imgsz=640, batch=10, device=[0,], workers=4, cache=True)
    model.export(format="onnx",dynamic=True,simplify=True)
#print(torch.cuda.device_count())

# ma= cv2.imshow('C:\\Users\\sleep\\Desktop\\R-C.png')
# cv2.imshow('ss',ma)
# cv2.waitKey(0)
