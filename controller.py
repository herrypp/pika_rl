from pynput.keyboard import Key
from pynput.keyboard import Controller as KeyboardController
import time

class Keyboard:
    def __init__(self):
        self.keyboard = KeyboardController()
        self.press_time = 0.2

    def sleep(self):
        time.sleep(self.press_time)

    def sleep_half(self):
        time.sleep(self.press_time / 2)

    def release(self):
        self.keyboard.release(Key.up)
        self.keyboard.release(Key.down)
        self.keyboard.release(Key.left)
        self.keyboard.release(Key.right)
        self.keyboard.release(Key.enter)

    def up(self):
        self.keyboard.press(Key.up)
        self.sleep()
        self.keyboard.release(Key.up)

    def down(self):
        self.keyboard.press(Key.down)
        self.sleep()
        self.keyboard.release(Key.down)

    def left(self):
        self.keyboard.press(Key.left)
        self.sleep()
        self.keyboard.release(Key.left)

    def right(self):
        self.keyboard.press(Key.right)
        self.sleep()
        self.keyboard.release(Key.right)

    def up_attack(self):
        self.keyboard.press(Key.up)
        self.keyboard.press(Key.enter)
        self.sleep()
        self.keyboard.release(Key.enter)
        self.keyboard.release(Key.up)

    def down_attack(self):
        self.keyboard.press(Key.down)
        self.keyboard.press(Key.enter)
        self.sleep()
        self.keyboard.release(Key.enter)
        self.keyboard.release(Key.down)

    def left_attack(self):
        self.keyboard.press(Key.left)
        self.keyboard.press(Key.enter)
        self.sleep()
        self.keyboard.release(Key.enter)
        self.keyboard.release(Key.left)

    def up_attack(self):
        self.keyboard.press(Key.right)
        self.keyboard.press(Key.enter)
        self.sleep()
        self.keyboard.release(Key.enter)
        self.keyboard.release(Key.right)

    def up_right_attack(self):
        self.keyboard.press(Key.up)
        self.keyboard.press(Key.right)
        self.keyboard.press(Key.enter)
        self.sleep()
        self.keyboard.release(Key.enter)
        self.keyboard.release(Key.right)
        self.keyboard.release(Key.up)

    def up_left_attack(self):
        self.keyboard.press(Key.up)
        self.keyboard.press(Key.left)
        self.keyboard.press(Key.enter)
        self.sleep()
        self.keyboard.release(Key.enter)
        self.keyboard.release(Key.left)
        self.keyboard.release(Key.up)

    def up_empty_attack(self):
        self.keyboard.press(Key.up)
        sleep_half()
        self.keyboard.release(Key.up)
        self.keyboard.press(Key.enter)
        self.sleep_half()
        self.keyboard.release(Key.enter)
        
    def press_command_c(self):
        self.keyboard.press(Key.cmd)
        self.keyboard.press('c')
        self.sleep_half()
        self.keyboard.release(Key.cmd)
        self.keyboard.release('c')

    def press_s(self):
        self.keyboard.press('s')
        self.sleep_half()
        self.keyboard.release('s')

    def press_h(self):
        self.keyboard.press('h')
        self.sleep_half()
        self.keyboard.release('h')

    def press_p(self):
        self.keyboard.press('p')
        self.sleep_half()
        self.keyboard.release('p')

    def press_a(self):
        self.keyboard.press('a')
        self.sleep_half()
        self.keyboard.release('a')

    def press_z(self):
        self.keyboard.press('z')
        self.sleep_half()
        self.keyboard.release('z')

    def press_enter(self):
        self.keyboard.press(Key.enter)
        self.sleep_half()
        self.keyboard.release(Key.enter)
