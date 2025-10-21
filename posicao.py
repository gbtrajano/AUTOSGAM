import pyautogui
import time

time.sleep(3)

x, y = pyautogui.position()
print(f'Sua posição X: {x} e Y: {y}')