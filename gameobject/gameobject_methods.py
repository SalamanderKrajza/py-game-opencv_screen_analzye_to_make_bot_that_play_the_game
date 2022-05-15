
from tkinter import X
import pyautogui 
import keyboard
import mss
import numpy as np
import cv2
import json
import ctypes
from time import sleep

def config(self):
    user32 = ctypes.windll.user32
    self.screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    self.height_of_middle_box = 133 #Height of middle box image
    self.top_start = 78 #Distance from top of screen to sound button
    self.how_many_levels_from_top = 2 #Describes which level we screenshoting (pick 0 for first entirely visible level)

    self.area_to_take_screenshot = {
        'entire_screen':{
            'left': 0, 
            'top': 0, 
            'width': self.screensize[0], 
            'height': self.screensize[1],
        },
        'default_area':{
            'left': 800, 
            'top': 560, 
            'width': 600, 
            'height': 300,
        },
        'game_area':{
            'left': 809, 
            'top': self.top_start, 
            'width': 580, 
            'height': self.screensize[1] - self.top_start, #137 is size of one middle box
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

def __init__(self):
    pyautogui.PAUSE = 0
    self.loop_number = 0
    self.quit_the_game = False
    self.screenshoot_tool = mss.mss()
    self.actionlist = ['left']
    self.previous_found_object = False
    # self.list_of_elements_on_top_levels = {
    #     'top1':[False, False, False, ],
    #     'top2':[False, False, ],
    #     'top3':[False,  ],
    # }
    self.list_of_elements_on_top_levels = {
        'top1':[False, ],
        'top2':[False, ],
        'top3':[False,  ],
    }
    self.threshold = 0.75
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
    self.desired_images[image_name]['matches'] = []
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
    if self.desired_images[image_name]['best_match_probability']>self.threshold:
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

def update_top_value_of_game_area(self):
    self.top_start = self.desired_images['corner']['best_match_position'][1]
    self.area_to_take_screenshot['game_area']['top'] = self.top_start
    self.area_to_take_screenshot['game_area']['height'] = self.screensize[1] - self.top_start #137 is size of one middle box

def highlight_levels(self):
    levels={
        'top1':{'position':[0,94+133*0], 'width':580, 'height':133, 'color':(0,255,255)},
        'top2':{'position':[0,94+133*1], 'width':580, 'height':133, 'color':(255,102,178)},
        'top3':{'position':[0,94+133*2], 'width':580, 'height':133, 'color':(51,0,25)},
    }
    for level in levels:
        cv2.rectangle(
            self.screenshot, 
            levels[level]['position'],  
            (
                levels[level]['position'][0] + levels[level]['width'],
                levels[level]['position'][1] + levels[level]['height']
            ), 
            levels[level]['color'], 
            2)

        cv2.putText(
            self.screenshot, 
            f"{level}: [{levels[level]['position']}", 
            (
                levels[level]['position'][0]+10,
                levels[level]['position'][1]+20
            ), 
            self.text_settings['font'], self.text_settings['fontScale'],
            levels[level]['color'], self.text_settings['thickness'], cv2.LINE_AA
        )


def check_if_quit_the_game(self):
    if keyboard.is_pressed('q'):
        print('\nGame is stopped')
        self.quit_the_game = True

    if self.desired_images['scoreboard']['best_match_probability']>self.threshold:
        print('\nGame is lost')
        self.quit_the_game = True

def update_level_values(self):
    matched_elements = {
        'top1':False,
        'top2':False,
        'top3':False,
    }
    for side in ['right', 'left']:
        target=f"{side}_box_icons"
        for match in self.desired_images[target]['matches']:
            if 94<match[1]<227:
                matched_elements['top1'] = side
            if 227<match[1]<360:
                matched_elements['top2'] = side
            if 360<match[1]<493:
                matched_elements['top3'] = side

    for level in matched_elements:
        self.list_of_elements_on_top_levels[level].insert(0, matched_elements[level])
    print(f'\nUpdated list of elements on top level sides: {json.dumps(self.list_of_elements_on_top_levels, indent=4)}')



def choose_side(self):
    probability_that_box_is_on_the_left = self.desired_images['left_box_icons']['best_match_probability']
    probability_that_box_is_on_the_right = self.desired_images['right_box_icons']['best_match_probability']
    if probability_that_box_is_on_the_left < self.threshold and probability_that_box_is_on_the_right < self.threshold:
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

def choose_side_by_lists(self):
    objects_before_moving={
        'top0':False,
        'top1':False,
        'top2':False,
        'top3':False,
        'top4':False,
        'rudy_level':False,
    }

    objects_after_moving = {
        'top0':False,
        'top1':False,
        'top2':False,
        'top3':False,
        'top4':objects_before_moving['top1'],
        'rudy_level':objects_before_moving['top2'],
    }


    self.side_package = {
        5:{'name':'top0', 'value':False,},
        4:{'name':'top1', 'value':False,},
        3:{'name':'top2', 'value':False,},
        2:{'name':'top3', 'value':False,},
        1:{'name':'top4', 'value':self.side_package ['top1'],}, #After making 3 moves it should have value values captured on previous screenshot
        0:{'name':'rudy_level', 'value':self.side_package ['top2'],},
    }

    
    for action_number in range(3):
        if self.side_package[action_number]:
        planned_actions.append()
    planned_actions = [False, False, False]
    


        self.current_found_object = self.previous_found_object
        for level in self.list_of_elements_on_top_levels:
            value_from_list = self.list_of_elements_on_top_levels[level].pop()
            if value_from_list: 
                self.current_found_object = value_from_list
                print(f'We picked valie {value_from_list} from {level} list')
        
        self.previous_found_object = self.current_found_object
        
        if self.current_found_object == 'right':
            self.choosen_side = 'left'
        elif self.current_found_object == 'left':
            self.choosen_side = 'right'
        else:
            self.choose_side=self.previous_found_object
        
