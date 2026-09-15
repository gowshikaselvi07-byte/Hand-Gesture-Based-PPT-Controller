import time
import pyautogui
import win32gui
import win32con

print("Open PowerPoint Slide Show...")
time.sleep(5)

windows = []

def find_window(hwnd, extra):
    title = win32gui.GetWindowText(hwnd)

    if "PowerPoint" in title:
        windows.append(hwnd)

win32gui.EnumWindows(find_window, None)

if windows:
    hwnd = windows[0]

    print("PowerPoint window found!")

    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)

    time.sleep(1)

    pyautogui.press("esc")

    print("ESC sent to PowerPoint!")

else:
    print("PowerPoint window NOT found!")