import keyboard
import pyautogui
from time import sleep
def test_arrowkeys():
    print("Press S to start")
    keyboard.wait('s')
    print('started')
    for x in range(3):
        keyboard.press_and_release('left')
        # pyautogui.press('left')
        sleep(0.2)


    for x in range(4):
        keyboard.press_and_release('right')
        # pyautogui.press('right')
        sleep(0.2)



# Problem jest taki, że chociaż w takim excelu wychwytuje KAŻDE kliknięcie to już w grze łapie tylko jedno na stronę
# test_arrowkeys()

def test_mouseclicks():

    target_position = {
        'left':{
            'x':709+200,
            'y':550,
        },
        'right':{
            'x':709+600,
            'y':550,
        }
    }

    print("Press S to start")
    keyboard.wait('s')
    print('started')
    for x in range(3):
        pyautogui.click(x = target_position['left']['x'], y= target_position['left']['y'])
    for x in range(4):
        pyautogui.click(x = target_position['right']['x'], y= target_position['right']['y'])

test_mouseclicks()