
from tkinter import X
import pyautogui 
import keyboard
import mss
import numpy as np
import cv2
import json
import ctypes
from time import sleep

class GameObject():
    def __init__(self):
        pyautogui.PAUSE = 0
        self.loop_number = 0
        self.quit_the_game = False
        self.screenshoot_tool = mss.mss()
        self.actionlist = ['left']
        self.config()

    def delete_previous_screenshots(self):
        import os
        import glob
        files = glob.glob('output/*.jpg')
        for f in files:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))



    def config(self):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

        self.height_of_middle_box = 133 #Height of middle box image
        self.top_start = 78 #Distance from top of screen to sound button
        self.highest_level_offset = 94 #Distance from top of the game to first complete level
        self.how_many_levels_from_top = 2 #Describes which level we screenshoting (pick 0 for first entirely visible level)

        self.area_to_take_screenshot = {
            'entire_screen':{
                'left': 0, 
                'top': 0, 
                'width': screensize[0], 
                'height': screensize[1],
            },
            'default_area':{
                'left': 800, 
                'top': 560, 
                'width': 600, 
                'height': 300,
            },
            'box_level':{
                'left': 809, 
                'top': self.top_start+self.highest_level_offset+self.height_of_middle_box*self.how_many_levels_from_top-50, 
                'width': 800, 
                'height': 237, #137 is size of one middle box
            },
        }

        self.text_settings = {
            'font':cv2.FONT_HERSHEY_SIMPLEX,
            'fontScale':0.5,
            'thickness':1,
        }

        self.desired_images = {
            'corner':{
                'path_to_sourcefile':'sourcefiles/corner.jpg',
                'image':False, 
                'width': False, 
                'height': False,
                'best_match_probability':False,
                'best_match_position':False,
                'color':(255,0,0),
                'matches':[],
            },
            'rudy':{
                'path_to_sourcefile':'sourcefiles/rudy.jpg',
                'image':False, 
                'width': False, 
                'height': False,
                'best_match_probability':False,
                'best_match_position':False,
                'color':(255,0,0),
                'matches':[],
            },
            'middle_box':{
                'path_to_sourcefile':'sourcefiles/middle_box.jpg',
                'image':False, 
                'width': False, 
                'height': False,
                'best_match_probability':False,
                'best_match_position':False,
                'color':(255,0,0),
                'matches':[],
            },
            'left_box_icons':{
                'path_to_sourcefile':'sourcefiles/left_box_icons.jpg',
                'image':False, 
                'width': False, 
                'height': False,
                'best_match_probability':False,
                'best_match_position':False,
                'color':(0,128,255), #orange
                'matches':[],
            },
            'right_box_icons':{
                'path_to_sourcefile':'sourcefiles/right_box_icons.jpg',
                'image':False, 
                'width': False, 
                'height': False,
                'best_match_probability':False,
                'best_match_position':False,
                'color':(255,0,255), #pink
                'matches':[],
            },
            'scoreboard':{
                'path_to_sourcefile':'sourcefiles/scoreboard.jpg',
                'image':False, 
                'width': False, 
                'height': False,
                'best_match_probability':False,
                'best_match_position':False,
                'color':(0,0,255),
                'matches':[],
            },
        }

        self.target_position = {
            'left':{
                'x':709+200,
                'y':550,
            },
            'right':{
                'x':709+600,
                'y':550,
            },

        }

    def load_image_to_reckognize(self, image_name):
        loaded_image = cv2.imread(self.desired_images[image_name]['path_to_sourcefile'])
        self.desired_images[image_name]['image'] = loaded_image
        self.desired_images[image_name]['width'] = loaded_image.shape[1]
        self.desired_images[image_name]['height'] = loaded_image.shape[0]

    def wait_to_start(self):
        print(
            "\nProgram is running!"
            "\nTo start playing press 'S' on your keyboard"
            "\nTo stop playing press 'Q' on your keyboard"
            )
        keyboard.wait('s')
        print('\nGame is started')
        
    def take_screenshot(self, target_area):
        """
        Version without removed alpha dont work with match [cv2.matchTemplate] method
        Version after removing alpha dont work with [cv2.rectangle] method
        """
        self.screenshot = np.array(self.screenshoot_tool.grab(self.area_to_take_screenshot[target_area]))
        self.screenshot_removed_alpha = self.screenshot[:,:,:3] 
        
    def find_matches_for_desired_image(self, image_name):
        #Analyze image
        result = cv2.matchTemplate(self.screenshot_removed_alpha, self.desired_images[image_name]['image'], cv2.TM_CCOEFF_NORMED)

        #Find and remember the best match
        _, probability, _, position = cv2.minMaxLoc(result)
        self.desired_images[image_name]['best_match_probability'] = probability
        self.desired_images[image_name]['best_match_position'] = position

        #Find and remember each match over given treshold
        threshold = 0.8
        matches_with_desired_treshold = np.where( result >= threshold)
        for position in zip(*matches_with_desired_treshold[::-1]):
            self.desired_images[image_name]['matches'].append(position)

    def highlight_on_screenshot(self, image_name, all_matches=False):
        if not all_matches:
            cv2.rectangle(
                self.screenshot, 
                self.desired_images[image_name]['best_match_position'],  
                (
                    self.desired_images[image_name]['best_match_position'][0] + self.desired_images[image_name]['width'],
                    self.desired_images[image_name]['best_match_position'][1] + self.desired_images[image_name]['height']
                ), 
                self.desired_images[image_name]['color'], 
                2)
        
        else:
            for match in self.desired_images[image_name]['matches']:
                cv2.rectangle(
                    self.screenshot, 
                    match,  
                    (
                        match[0] + self.desired_images[image_name]['width'], 
                        match[1] + self.desired_images[image_name]['height']
                    ), 
                    self.desired_images[image_name]['color'], 
                    2)

    def show_clicking_areas(self):
        for target_side in ('left', 'right'):
            cv2.circle(
                self.screenshot, 
                (
                    self.target_position[target_side]['x'],
                    self.target_position[target_side]['y']
                ), 
                30, 
                (0,255,0), 
                5
            )

    def print_matches_info(self, image_name):
        print(
            f"Item name  - {image_name:20s}"
            f"Item size  - H:{self.desired_images[image_name]['height']:4d} ; W:{self.desired_images[image_name]['width']:4d} "
            f"Best_match probability - {self.desired_images[image_name]['best_match_probability']:0.2f} "
            f"Best_match position - {self.desired_images[image_name]['best_match_position']} "
            f"Number of matches - {len(self.desired_images[image_name]['matches'])} "
            )
   


    def put_text_on_highlight(self, image_name):
        cv2.putText(
            self.screenshot, 
            f"{image_name}: [{self.desired_images[image_name]['best_match_probability']:0.2f}]; {self.desired_images[image_name]['best_match_position']}", 
            (
                self.desired_images[image_name]['best_match_position'][0]+10,
                self.desired_images[image_name]['best_match_position'][1]+20
            ), 
            self.text_settings['font'], self.text_settings['fontScale'],
            self.desired_images[image_name]['color'], self.text_settings['thickness'], cv2.LINE_AA
        )

    def save_screenshot(self, bonus_name=""):
        cv2.imwrite(f'output\output{self.loop_number}{bonus_name}.jpg', self.screenshot)    

    def update_top_value_of_box_level(self):
        self.top_start = self.desired_images['corner']['best_match_position'][1]
        self.area_to_take_screenshot['box_level']['top'] = self.top_start+self.highest_level_offset+self.height_of_middle_box*self.how_many_levels_from_top-50

    def check_if_quit_the_game(self):
        if keyboard.is_pressed('q'):
            print('\nGame is stopped')
            self.quit_the_game = True

        if self.desired_images['scoreboard']['best_match_probability']>0.70:
            print('\nGame is lost')
            self.quit_the_game = True

    def choose_side(self):
        probability_that_box_is_on_the_left = self.desired_images['left_box_icons']['best_match_probability']
        probability_that_box_is_on_the_right = self.desired_images['right_box_icons']['best_match_probability']
        if probability_that_box_is_on_the_left < 0.75 and probability_that_box_is_on_the_right < 0.75:
            self.choosen_side = self.actionlist[0] #If we cant determine which side we should choose then repead previous one
            print(f'Choosen side is by picking previous decision: {self.choosen_side}')
        else:
            if probability_that_box_is_on_the_left>probability_that_box_is_on_the_right:
                self.choosen_side = 'right'
                side_with_object = 'left'
            else:
                self.choosen_side = 'left'
                side_with_object = 'right'
            print(f'Choosen side is by picking higher probability: {self.choosen_side}')

            #Extra check if best match is inside checked area:
            if not(180 > self.desired_images[f'{side_with_object}_box_icons']['best_match_position'][1] > 55):
                self.choosen_side = self.actionlist[0] #If we cant determine which side we should choose then repead previous one
                print(f'Choosen side is by replaced with previous decision: [{self.choosen_side}] because of wrong place of matching')

    def game_loop(self):
        self.delete_previous_screenshots()
        for image in self.desired_images:
            self.load_image_to_reckognize(image)

        self.wait_to_start()
        self.take_screenshot(target_area='entire_screen')
        for target in ('corner', 'middle_box'):
            self.find_matches_for_desired_image(target)
            self.highlight_on_screenshot(target, all_matches=True)
            self.put_text_on_highlight(target)
            self.print_matches_info(target)
        self.show_clicking_areas()
        self.save_screenshot()
        
        self.update_top_value_of_box_level()

        sleep_time = 0.05
        while not self.quit_the_game:
            self.loop_number+=1
            print(f'\nloop_number: {self.loop_number}')

            #Just for debuging
            self.take_screenshot(target_area='entire_screen')
            self.save_screenshot('-e')

            self.take_screenshot(target_area='box_level')
            for target in ('right_box_icons', 'left_box_icons', 'scoreboard'):
                self.find_matches_for_desired_image(target)
                self.highlight_on_screenshot(target)
                self.put_text_on_highlight(target)
                self.print_matches_info(target)
            self.choose_side()
            if self.choosen_side=='right':
                self.actionlist.insert(0, 'right')
            else:
                self.actionlist.insert(0, 'left')
            self.save_screenshot()

            print(f'Currently planned actions are: {self.actionlist}')

            target_side = self.actionlist.pop()
            pyautogui.click(x = self.target_position[target_side]['x'], y= self.target_position[target_side]['y'])
            
            if self.loop_number%100==0: 
                sleep_time-=0.01
            if self.loop_number>200 and self.loop_number%10==0: 
                sleep_time-=0.003
            elif self.loop_number>250 and self.loop_number%10==0: 
                sleep_time-=0.004
            sleep(sleep_time)
            self.check_if_quit_the_game()

GO = GameObject()
GO.game_loop()
            




