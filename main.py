import keyboard
import mss
import cv2
import numpy
from time import time, sleep
import pyautogui 

pyautogui.PAUSE = 0

print("Press 's' to start playing.")
print("Once started press 'q' to quit.")
keyboard.wait('s')

left = True
target_position = {
    'x':850,
    'y':550,
}
screenshoot_tool = mss.mss()

area_to_make_screenshot_of_left_side = {'left': 800, 'top': 460, 'width': 600, 'height': 400}
area_to_make_screenshot_of_right_side = {'left': 800, 'top': 460, 'width': 600, 'height': 400}

pack_left = cv2.imread('data/left_pack.jpg')
pack_right = cv2.imread('data/right_pack.jpg')
size_of_highlight_area = {
    'width':pack_left.shape[1],
    'height':pack_left.shape[0]
}

fps_time = time()
cnt=1
while True:
    if left:
        screenshot = numpy.array(screenshoot_tool.grab(area_to_make_screenshot_of_left_side))
        wood = pack_left
    else:
        screenshot = numpy.array(screenshoot_tool.grab(area_to_make_screenshot_of_right_side))
        wood = pack_right
    # Cut off alpha
    scr_remove = screenshot[:,:,:3]
    # with mss.mss() as mss_instance:  # Create a new mss.mss instance
    #     monitor_1 = mss_instance.monitors[1]  # Identify the display to capture
    #     screenshot = mss_instance.grab(monitor_1)  # Take the screenshot
    #     img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")  # Convert to PIL.Image
    #     img.show()  # Show the image using the default image viewer
    # cv2.imshow('a crop of the screen', scr_remove)
    result = cv2.matchTemplate(scr_remove, wood, cv2.TM_CCOEFF_NORMED)

    _, probability_of_matching, _, position_of_matched_image = cv2.minMaxLoc(result)
    print(f"probability_of_matching: {probability_of_matching:2f} position_of_matched_image: {position_of_matched_image}")
    # src = screenshot.copy()
    if probability_of_matching > .50:
        left = not left
        if left:
            target_position['x'] = 850
        else:
            target_position['x'] = 1200
        cv2.rectangle(screenshot, position_of_matched_image, (position_of_matched_image[0] + size_of_highlight_area['width'], position_of_matched_image[1] + size_of_highlight_area['height']), (0,255,255), 2)

    cv2.imshow('Screen Shot', screenshot)
    cv2.imwrite(f'data\output{cnt}.jpg', scr_remove)    
    cnt+=1
    cv2.imwrite('data\output_wood.jpg', wood)    
    cv2.waitKey(1)
    pyautogui.click(x = target_position['x'], y= target_position['y'])
    sleep(.10)
    if keyboard.is_pressed('q'):
        break

    print('FPS: {}'.format(1 / (time() - fps_time)))
    fps_time = time()