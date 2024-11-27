import cv2
import pyautogui
from pynput import mouse
from ultralytics import YOLO
import numpy as np
import wind
import os
import threading
import win32con
import  win32api

# 加载模型
model = YOLO('cs.pt')  # 适配相应的环境和模型路径
cv2.namedWindow('Detected Objects', cv2.WINDOW_AUTOSIZE)
count = 0
# 初始化全局变量
moveX, moveY = 0, 0
listener = None  # 必须初始化 listener


def detect_and_draw_boxes():
    global moveX, moveY, listener,closest_center,count # 将其声明为全局变量
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
    # count+=1
    # directory = 'datasets/test/'
    # file_name = f'{count}.png'
    # file_path = os.path.join(directory, file_name)
    # cv2.imwrite(file_path,image)

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
        if button == mouse.Button.left and pressed and moveX != 0:
            # 获取当前鼠标位置
            current_x, current_y = win32api.GetCursorPos()
            # 计算要移动的目标位置
            target_x = moveX+2560/2
            target_y = moveY+1600/2
            # 移动鼠标到目标位置
            win32api.SetCursorPos((int(target_x), int(target_y)))

            listener.stop()  # 停止当前的监听器
            # 重新启动监听器（谨慎使用递归启动以避免堆栈溢出）
            launch_mouse_listener(moveX, moveY)

    listener = mouse.Listener(on_click=move_and_restart)
    listener.start()


while True:
 detect_and_draw_boxes()
