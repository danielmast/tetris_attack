# Third party imports
import cv2
import numpy as np
import win32gui
import win32ui
import win32con

WINDOW_NAME = 'Tetris Attack (U) [!] - Snes9x 1.60'


def capture_gamewindow():
    hwnd = win32gui.FindWindow(None, WINDOW_NAME)
    hwndex = win32gui.FindWindowEx(hwnd, 0, WINDOW_NAME, None)
    hwnddc = win32gui.GetWindowDC(hwndex)
    srcdc = win32ui.CreateDCFromHandle(hwnddc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()

    x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
    width = x2 - x1
    height = y2 - y1

    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (x1, y1), win32con.SRCCOPY)

    signed_integers_array = bmp.GetBitmapBits(True)
    img = np.fromstring(signed_integers_array, dtype='uint8')
    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnddc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    #return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)