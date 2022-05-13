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

left_clear = True
target_side='left'
target_position = {
    'left':{
        'x':850,
        'y':550,
    },
    'right':{
        'x':1200,
        'y':550,
    },

}
screenshoot_tool = mss.mss()

area_to_make_screenshot_of_left_side = {'left': 800, 'top': 560, 'width': 600, 'height': 300}
area_to_make_screenshot_of_right_side = {'left': 800, 'top': 560, 'width': 600, 'height': 300}

left_clear_area_image = cv2.imread('data/left_clear_area2.jpg')
right_clear_area_image = cv2.imread('data/right_clear_area2.jpg')
size_of_highlight_area = {
    'width':left_clear_area_image.shape[1],
    'height':left_clear_area_image.shape[0]
}



left_pack_image = cv2.imread('data/left_pack.jpg')
right_pack_image = cv2.imread('data/right_pack.jpg')
size_of_highlight_area2 = {
    'width':left_pack_image.shape[1],
    'height':left_pack_image.shape[0]
}


fps_time = time()
cnt=1
while True:
    screenshot = numpy.array(screenshoot_tool.grab(area_to_make_screenshot_of_left_side))
    object_to_find = right_clear_area_image
    # Cut off alpha
    scr_remove = screenshot[:,:,:3]
    # with mss.mss() as mss_instance:  # Create a new mss.mss instance
    #     monitor_1 = mss_instance.monitors[1]  # Identify the display to capture
    #     screenshot = mss_instance.grab(monitor_1)  # Take the screenshot
    #     img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")  # Convert to PIL.Image
    #     img.show()  # Show the image using the default image viewer
    # cv2.imshow('a crop of the screen', scr_remove)
    
    #Check if left empty area is empty
    results = {
        'left_clear_area_image':{'probability_of_matching':'', 'position_of_matched_image':'', 'image':left_clear_area_image},
        'right_clear_area_image':{'probability_of_matching':'', 'position_of_matched_image':'', 'image':right_clear_area_image},
        'left_pack_image':{'probability_of_matching':'', 'position_of_matched_image':'', 'image':left_pack_image},
        'right_pack_image':{'probability_of_matching':'', 'position_of_matched_image':'', 'image':right_pack_image},
    }

    for key in results:
        result = cv2.matchTemplate(scr_remove, results[key]['image'], cv2.TM_CCOEFF_NORMED)
        _, results[key]['probability_of_matching'], _, results[key]['position_of_matched_image'] = cv2.minMaxLoc(result)
        print(f"output{cnt} - {key} - probability_of_matching: {results[key]['probability_of_matching']:0.2f} position_of_matched_image: {results[key]['position_of_matched_image']}")

    # result = cv2.matchTemplate(scr_remove, right_clear_area_image, cv2.TM_CCOEFF_NORMED)
    # _, probability_of_matching_on_right, _, position_of_matched_image = cv2.minMaxLoc(result)

    # result = cv2.matchTemplate(scr_remove, left_pack_image, cv2.TM_CCOEFF_NORMED)
    # _, probability_of_left_pack_image, _, position_of_matched_image = cv2.minMaxLoc(result)

    # result = cv2.matchTemplate(scr_remove, right_pack_image, cv2.TM_CCOEFF_NORMED)
    # _, probability_of_right_pack_image, _, position_of_matched_image = cv2.minMaxLoc(result)
    
    
    # print(f"output{cnt} - probability_of_matching_on_left: {probability_of_matching_on_left:0.2f} position_of_matched_image: {position_of_matched_image}")
    # print(f"output{cnt} - probability_of_matching_on_right: {probability_of_matching_on_right:0.2f} position_of_matched_image: {position_of_matched_image}")
    # print(f"output{cnt} - probability_of_matching_on_left: {probability_of_left_pack_image:0.2f} position_of_matched_image: {position_of_matched_image}")
    # print(f"output{cnt} - probability_of_matching_on_right: {probability_of_right_pack_image:0.2f} position_of_matched_image: {position_of_matched_image}")



    # src = screenshot.copy()
    left_clear = results['left_clear_area_image']['probability_of_matching']
    right_clear = results['right_clear_area_image']['probability_of_matching']
    diff1 = left_clear - right_clear
    right_pack = results['right_pack_image']['probability_of_matching']
    left_pack = results['left_pack_image']['probability_of_matching']
    diff2 = right_pack - left_pack
    if (right_pack+left_pack) > 120:
        diff2 = diff2*12
    elif (right_pack+left_pack) > 20:
        diff2 = diff2*6
    else:
        diff2 = diff2*2
    if (diff1+diff2) > (0):
        print(f'Left clear: {diff1:0.2f}+{diff2:0.2f}={(diff1+diff2):0.2f}>0')
        position_of_matched_image = results['left_clear_area_image']['position_of_matched_image']
        target_side = 'left'
    else:
        print(f'Right clear: {diff1:0.2f}+{diff2:0.2f}={(diff1+diff2):0.2f}<0')
        position_of_matched_image = results['right_clear_area_image']['position_of_matched_image']
        target_side = 'right'
    # if results['right_pack_image']['probability_of_matching']>0.95:
    #     print('decided by right_pack')
    #     target_side='left'
    #     position_of_matched_image = results['right_pack_image']['position_of_matched_image']
    #     cv2.rectangle(screenshot, position_of_matched_image, (position_of_matched_image[0] + size_of_highlight_area2['width'], position_of_matched_image[1] + size_of_highlight_area2['height']), (0,255,255), 2)
    # elif results['left_pack_image']['probability_of_matching']>0.95:
    #     print('decided by left_pack')
    #     position_of_matched_image = results['left_pack_image']['position_of_matched_image']
    #     cv2.rectangle(screenshot, position_of_matched_image, (position_of_matched_image[0] + size_of_highlight_area2['width'], position_of_matched_image[1] + size_of_highlight_area2['height']), (0,255,255), 2)
    #     target_side='right'
    # else:
    #     if results['left_clear_area_image']['probability_of_matching'] > results['right_clear_area_image']['probability_of_matching']:
    #         print('decided by left_area')
    #         position_of_matched_image = results['left_clear_area_image']['position_of_matched_image']
    #         target_side = 'left'
    #     else:
    #         print('decided by right_area')
    #         position_of_matched_image = results['right_clear_area_image']['position_of_matched_image']
    #         target_side = 'right'

    print('\n')
    # if left_clear:
    #     target_position['x'] = 1200
    # else:
    #     target_position['x'] = 850
    # cv2.rectangle(screenshot, position_of_matched_image, (position_of_matched_image[0] + size_of_highlight_area2['width'], position_of_matched_image[1] + size_of_highlight_area2['height']), (255,0,255), 2)

    # cv2.imshow('Screen Shot', screenshot)
    cv2.imwrite(f'data\output{cnt}.jpg', scr_remove)    
    cnt+=1
    cv2.imwrite('data\output_object_to_find.jpg', object_to_find)    
    cv2.waitKey(1)
    print(f"pressed {target_side} side\n\n")
    pyautogui.click(x = target_position[target_side]['x'], y= target_position[target_side]['y'])
    sleep(.07)
    if keyboard.is_pressed('q'):
        break

    print('FPS: {}'.format(1 / (time() - fps_time)))
    fps_time = time()