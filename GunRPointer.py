import pyautogui
import time
from math import sqrt
from pynput import mouse, keyboard
from pynput.keyboard import Key, Controller
import threading

pyautogui.FAILSAFE = False

print("Welcome to GunRPointer - Control FPS with Mouse V.01 (WIP)")
print("Click on window's game to active focus and control game with your mouse.")
print("Left Click to shoot and Right Click to target (see readme)")
print("Press ESC to exit")

# Drapeau pour contrôler l'exécution de la boucle
running = True

# État des touches
keys_pressed = {
    Key.up: False,
    Key.down: False,
    Key.left: False,
    Key.right: False
}

# Création du contrôleur de clavier
keyboard_controller = Controller()

# Définition de la résolution de l'écran
screen_width, screen_height = pyautogui.size()
centre_x, centre_y = screen_width / 2, screen_height / 2

# Zone de tolérance autour du centre
tolerance = 13  # Tolérance de 13 pixels autour du centre

def is_cursor_near_center_x(x):
    return centre_x - tolerance <= x <= centre_x + tolerance

def is_cursor_near_center_y(y):
    return centre_y - tolerance <= y <= centre_y + tolerance

def press_key(key):
    if not keys_pressed[key]:
        keyboard_controller.press(key)
        keys_pressed[key] = True

def release_key(key):
    if keys_pressed[key]:
        keyboard_controller.release(key)
        keys_pressed[key] = False

def release_all_keys():
    for key in keys_pressed.keys():
        release_key(key)

def on_mouse_click(x, y, button, pressed):
    if button == mouse.Button.left:
        if pressed:
            keyboard_controller.press('w')
        else:
            keyboard_controller.release('w')
    elif button == mouse.Button.right:
        if pressed:
            release_all_keys()
            keyboard_controller.press('e')
        else:
            keyboard_controller.release('e')

def on_mouse_move(x, y):
    if not is_cursor_near_center_x(x):
        if x < centre_x:
            press_key(Key.left)
        else:
            release_key(Key.left)
        if x > centre_x:
            press_key(Key.right)
        else:
            release_key(Key.right)
    else:
        release_key(Key.left)
        release_key(Key.right)

    if not is_cursor_near_center_y(y):
        if y < centre_y:
            press_key(Key.up)
        else:
            release_key(Key.up)
        if y > centre_y:
            press_key(Key.down)
        else:
            release_key(Key.down)
    else:
        release_key(Key.up)
        release_key(Key.down)

def check_cursor_position():
    while running:
        x, y = pyautogui.position()
        if is_cursor_near_center_x(x):
            release_key(Key.left)
            release_key(Key.right)
        if is_cursor_near_center_y(y):
            release_key(Key.up)
            release_key(Key.down)
        time.sleep(0.1)  # Vérification toutes les 100 ms

def on_key_press(key):
    global running
    #try:
        #print(f"Touche pressée: {key.char}")
    #except AttributeError:
        #print(f"Touche spéciale pressée: {key}")

    if key == keyboard.Key.esc:
        running = False

mouse_listener = mouse.Listener(on_click=on_mouse_click, on_move=on_mouse_move)
key_listener = keyboard.Listener(on_press=on_key_press)

mouse_listener.start()
key_listener.start()

cursor_check_thread = threading.Thread(target=check_cursor_position)
cursor_check_thread.start()

def calculate_attraction_force(x, y):
    distance_x = centre_x - x
    distance_y = centre_y - y
    distance = sqrt(distance_x**2 + distance_y**2)

    if distance == 0:
        return 0, 0

    force_x = distance_x / distance * distance
    force_y = distance_y / distance * distance

    return force_x, force_y

while running:
    mouse_x, mouse_y = pyautogui.position()
    force_x, force_y = calculate_attraction_force(mouse_x, mouse_y)

    pyautogui.moveRel(force_x, force_y)
    time.sleep(0.01)

    #print(f"Position du curseur: {mouse_x}, {mouse_y}")

mouse_listener.stop()
key_listener.stop()
cursor_check_thread.join()
#print("Script terminé.")
