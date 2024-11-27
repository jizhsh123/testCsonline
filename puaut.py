import cv2
import pyautogui
from pynput import mouse
from ultralytics import YOLO
import numpy as np
import wind
import threading

# 加载模型
model = YOLO('cs.pt')  # 适配相应的环境和模型路径
cv2.namedWindow('Detected Objects', cv2.WINDOW_AUTOSIZE)

# 初始化全局变量
moveX, moveY = 0, 0
listener = None  # 必须初始化 listener


def detect_and_draw_boxes():
    global moveX, moveY, listener,closest_center  # 将其声明为全局变量
    centers = []
    image = wind.getimage()
    results = model(image)
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            confidence = box.conf[0].item()
            cls = box.cls[0].item()
            centers.append(((x1 + x2) / 2, (y1 + y2) / 2))
            label = f'{model.names[int(cls)]} {confidence:.2f}'
            color = (255, 0, 0)  # 蓝色
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(image, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow('Detected Objects', image)
    cv2.waitKey(1)

    target_point = (320, 320)
    min_distance = float('inf')
    closest_center = None

    for center in centers:
        distance = np.sqrt((center[0] - target_point[0]) ** 2 + (center[1] - target_point[1]) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_center = center

    if closest_center is not None:
        moveX = closest_center[0] - target_point[0]
        moveY = closest_center[1] - target_point[1]

        if listener is None:  # 仅在监听器未启动时启动
            launch_mouse_listener(moveX, moveY)

        closest_center = None
    else:
        moveX=0
def launch_mouse_listener(x, y):
    global listener  # 再次声明它为全局变量

    def move_and_restart(x, y, button, pressed):
        if button == mouse.Button.right and pressed and moveX !=0:
            screenWidth, screenHeight = pyautogui.size()
            pyautogui.moveTo(screenWidth / 2+moveX, screenHeight / 2+moveY-20, duration=0.1)
            #pyautogui.move(moveX, moveY, duration=0.1)

            listener.stop()  # 停止监听器
            launch_mouse_listener(moveX,moveY)

    listener = mouse.Listener(on_click=move_and_restart)
    listener.start()


while True:
    detect_and_draw_boxes()