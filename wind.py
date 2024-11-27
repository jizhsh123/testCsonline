import pyautogui
import numpy as np
import  cv2


# 设置捕获电脑区域
centerXL=2560/2-320
centerYL=1600/2-320
region = (960, 480,640 , 640)

def getimage():
    # 创建 windows 窗体
    #cv2.namedWindow("Real-time Screen Capture", cv2.WINDOW_AUTOSIZE)

    # 设置捕获对象
    screenshot = pyautogui.screenshot(region=region)
    screenshot_np = np.array(screenshot)

    # 将 BGR 转换为 RGB (OpenCV 默认使用 RGB)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
    return  screenshot_np
    # cv2.imshow("Real-time Screen Capture", screenshot_np)
    # cv2.waitKey(0)





