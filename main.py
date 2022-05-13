
import pyautogui 
import keyboard

class GameObject():
    def __init__(self):
        pyautogui.PAUSE = 0
        self.quit_the_game = False

    def wait_to_start(self):
        print(
            "\nProgram is running!"
            "\nTo start playing press 'S' on your keyboard"
            "\nTo stop playing press 'Q' on your keyboard"
            )
        keyboard.wait('s')
        print('\nGame is started')

    def check_if_quit_the_game(self):
        if keyboard.is_pressed('q'):
            print('\nGame is stopped')
            self.quit_the_game = True

    def game_loop(self):
        self.wait_to_start()
        while not self.quit_the_game:
            self.check_if_quit_the_game()

GO = GameObject()
GO.game_loop()
            




