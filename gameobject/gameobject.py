class GameObject():
    from gameobject.gameobject_methods import config

    from gameobject.gameobject_methods import __init__, delete_previous_screenshots, load_image_to_reckognize, wait_to_start, take_screenshot
    from gameobject.gameobject_methods import find_matches_for_desired_image, highlight_on_screenshot, show_clicking_areas, print_matches_info, put_text_on_highlight
    from gameobject.gameobject_methods import save_screenshot, update_top_value_of_game_area, highlight_levels, check_if_quit_the_game, update_level_values, choose_side
    from gameobject.gameobject_methods import choose_side_by_lists
    
        
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
        self.save_screenshot('-e')
        
        self.update_top_value_of_game_area()

        self.take_screenshot(target_area='game_area')
        self.highlight_levels()
        self.save_screenshot()

        sleep_time = 0.05
        while not self.quit_the_game:
            self.loop_number+=1
            print(f'\nloop_number: {self.loop_number}')

            self.take_screenshot(target_area='game_area')
            for target in ('right_box_icons', 'left_box_icons', 'scoreboard'):
                self.find_matches_for_desired_image(target)
                self.highlight_on_screenshot(target, all_matches=True)
                self.put_text_on_highlight(target)
                self.print_matches_info(target)

            self.update_level_values()
            
            self.choose_side_by_lists()

            self.highlight_levels()
            self.save_screenshot()

            print(f'Currently planned actions are: {self.choosen_side}')

            target_side = self.choosen_side
            pyautogui.click(x = self.target_position[target_side]['x'], y= self.target_position[target_side]['y'])
            
            if self.loop_number%100==0: 
                sleep_time-=0.01
            if self.loop_number>200 and self.loop_number%10==0: 
                sleep_time-=0.003
            elif self.loop_number>250 and self.loop_number%10==0: 
                sleep_time-=0.004
            sleep(sleep_time)
            self.check_if_quit_the_game()

                # self.quit_the_game=True