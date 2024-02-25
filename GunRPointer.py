import pyautogui
import time
from math import sqrt
from pynput import mouse, keyboard
from pynput.keyboard import Key, Controller, Listener
import threading
from threading import Timer
import sys
import configparser
import psutil
import logging

# Variables globales
logging.basicConfig(level=logging.INFO)

running = True
absolute_mode = False
mouse_moved = False
pyautogui.FAILSAFE = False

INI_DELAY_RELEASE_AFTER_PRESS = 0.05
INI_DOUBLE_CLICK_TIMING = 0.2
INI_REFRESH_CHECK_POSITION = 0.1
# spring / friction / elastic / gravitational / tension
INI_FORCE_TYPE_DEFAULT_MODE_X = 'spring'
INI_FORCE_TYPE_DEFAULT_MODE_Y = 'positive'
INI_FORCE_TYPE_ABSOLUTE_MODE_X = 'elastic'
INI_FORCE_TYPE_ABSOLUTE_MODE_Y = 'elastic'

INI_FORCE_CONSTANT_X = 0
INI_FORCE_FACTOR_X = 1
INI_FORCE_CONSTANT_Y = 0
INI_FORCE_FACTOR_Y = 1
INI_FORCE_CONSTANT_ABSOLUTE_MODE_X = 0
INI_FORCE_FACTOR_ABSOLUTE_MODE_X = 1
INI_FORCE_CONSTANT_ABSOLUTE_MODE_Y = 0
INI_FORCE_FACTOR_ABSOLUTE_MODE_Y = 1

INI_INVERSE_Y = False

INI_TOLERANCE_DEFAULT_MODE_X = 3
INI_TOLERANCE_DEFAULT_MODE_Y = 30
INI_TOLERANCE_ABSOLUTE_MODE_X = 1
INI_TOLERANCE_ABSOLUTE_MODE_Y = 1

INI_REFRESH_FORCE_CALCUL = 0.01
#vertical / horizontal / omnidirectional in relative pointer mode
INI_MOVING_MODE_DEFAULT = 'omnidirectional'
#vertical / horizontal / omnidirectional in absolute pointer mode
INI_MOVING_MODE_TARGETZOOM = 'omnidirectional'

USE_RELEASE_ALL_KEYS_SIMPLE_CLICK_LEFT = False
USE_RELEASE_ALL_KEYS_SIMPLE_CLICK_MIDDLE = False
USE_RELEASE_ALL_KEYS_SIMPLE_CLICK_RIGHT = True
USE_RELEASE_ALL_KEYS_DOUBLE_CLICK_LEFT = False
USE_RELEASE_ALL_KEYS_DOUBLE_CLICK_MIDDLE = False
USE_RELEASE_ALL_KEYS_DOUBLE_CLICK_RIGHT = False
USE_RELEASE_ALL_KEYS_RELEASE_CLICK_LEFT = False
USE_RELEASE_ALL_KEYS_RELEASE_CLICK_MIDDLE = False
USE_RELEASE_ALL_KEYS_RELEASE_CLICK_RIGHT = False
USE_RELEASE_ALL_KEYS_SCROLL_UP = False
USE_RELEASE_ALL_KEYS_SCROLL_DOWN = False

USE_ABSOLUTE_MODE_SIMPLE_CLICK_LEFT = False
USE_ABSOLUTE_MODE_SIMPLE_CLICK_MIDDLE = False
USE_ABSOLUTE_MODE_SIMPLE_CLICK_RIGHT = True
USE_ABSOLUTE_MODE_DOUBLE_CLICK_LEFT = False
USE_ABSOLUTE_MODE_DOUBLE_CLICK_MIDDLE = False
USE_ABSOLUTE_MODE_DOUBLE_CLICK_RIGHT = False
USE_ABSOLUTE_MODE_RELEASE_CLICK_LEFT = False
USE_ABSOLUTE_MODE_RELEASE_CLICK_MIDDLE = False
USE_ABSOLUTE_MODE_RELEASE_CLICK_RIGHT = False
USE_ABSOLUTE_MODE_SCROLL_UP = False
USE_ABSOLUTE_MODE_SCROLL_DOWN = False

KEY_CLICK_LEFT = 'w'
KEY_CLICK_MIDDLE = 'x'
KEY_CLICK_RIGHT = 'e'
KEY_DOUBLE_CLICK_LEFT = 'z'
KEY_DOUBLE_CLICK_MIDDLE = 'a'
KEY_DOUBLE_CLICK_RIGHT = 'q'
KEY_SCROLL_UP = 's'
KEY_SCROLL_DOWN = 'd'

tolerance_default_x = 0
tolerance_default_y = 0
tolerance_absolute_x = 0
tolerance_absolute_y = 0

config = configparser.ConfigParser()

def load_config_mapper(system, game):
    # Obtention du répertoire de travail actuel
    current_working_dir = os.getcwd()
    # Remonter puis redescendre jusqu'à au ini du plugin
    current_working_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_working_dir))))
    current_working_dir = os.path.join(current_working_dir, 'plugins', 'GunRPointer')
    # Construction du chemin vers le fichier INI spécifique au jeu
    ini_path = os.path.join(current_working_dir, 'mappers', system, f"{game}.ini")

    # Vérification de l'existence du fichier INI spécifique
    if not os.path.exists(ini_path):
        logging.info(f"Fichier INI {ini_path} spécifique non trouvé pour {system}/{game}, utilisation du fichier par défaut.")
        sys.exit(1)
        # Si non trouvé, utilisation du chemin du fichier INI par défaut
        #ini_path = os.path.join(current_working_dir, 'mappers', 'default.ini')

    # Affichage du chemin du fichier INI pour le débogage
    print(f"Chemin du fichier INI: {ini_path}")

    # Lecture du fichier INI
    config = configparser.ConfigParser()
    config.read(ini_path)
    return config

def extract_game_and_system(args):
    game = next((arg.split("=")[1] for arg in args if "--game" in arg), "")
    system = next((arg.split("=")[1] for arg in args if "--system" in arg), "")
    return game, system

def initialize_mouse_and_keyboard_control():
    global running, keys_pressed, keyboard_controller, screen_width, screen_height, centre_x, centre_y, tolerance_default_x, tolerance_default_y, tolerance_absolute_x, tolerance_absolute_y

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

    # Zones de tolérance autour du centre (en pourcentage de la largeur et de la hauteur de l'écran)
    tolerance_default_x = (INI_TOLERANCE_DEFAULT_MODE_X / 100.0) * screen_width
    tolerance_default_y = (INI_TOLERANCE_DEFAULT_MODE_Y / 100.0) * screen_height
    tolerance_absolute_x = (INI_TOLERANCE_ABSOLUTE_MODE_X / 100.0) * screen_width
    tolerance_absolute_y = (INI_TOLERANCE_ABSOLUTE_MODE_Y / 100.0) * screen_height

def check_if_already_running():
    current_process_name = "GunRPointer.exe"
    process_count = 0

    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == current_process_name:
            process_count += 1

    if process_count > 2:  # Il y a plus d'une instance, y compris celle-ci
        logging.info("Une autre instance de GunRPointer est déjà en cours d'exécution. Exiting.")
        sys.exit(1)

key_press_times = {}
key_press_times_lock = threading.Lock()
def press_and_release_after_delay(key, delay=0.05):
    global key_press_times
    with key_press_times_lock:
        current_time = time.time()
        keyboard_controller.press(key)
        key_press_times[key] = current_time

    def release_key_after_delay():
        time.sleep(delay)
        with key_press_times_lock:
            if key in key_press_times:
                keyboard_controller.release(key)
                key_press_times.pop(key, None)

    threading.Thread(target=release_key_after_delay).start()

def is_cursor_near_center_x(x):
    global absolute_mode
    if absolute_mode: return centre_x - tolerance_absolute_x <= x <= centre_x + tolerance_absolute_x
    else: return centre_x - tolerance_default_x <= x <= centre_x + tolerance_default_x

def is_cursor_near_center_y(y):
    global absolute_mode
    if absolute_mode: return centre_y - tolerance_absolute_y <= y <= centre_y + tolerance_absolute_y
    else: return centre_y - tolerance_default_y <= y <= centre_y + tolerance_default_y

def release_all_keys():
    for key in keys_pressed.keys():
        release_key(key)

def press_key(key, record_action=False):
    #print(f"Fonction press_key : {key}")
    global actions_enregistrees, keys_pressed, absolute_mode
    current_time = time.time()

    if not keys_pressed.get(key, False):
        keyboard_controller.press(key)
        keys_pressed[key] = True

        if record_action and absolute_mode:
            # Enregistrer l'action
            actions_enregistrees.append((key, current_time))
            print(f"Action enregistrée : {key} pressée à {current_time}")

def release_key(key, record_action=False):
    #print(f"Fonction release_key : {key}")
    global actions_enregistrees, absolute_mode
    if keys_pressed.get(key, False):
        keyboard_controller.release(key)
        keys_pressed[key] = False

        if record_action and absolute_mode:
            # Calculer la durée et mettre à jour l'action
            for i, action in enumerate(actions_enregistrees):
                if action[0] == key and len(action) == 2:
                    start_time = action[1]
                    duration = time.time() - start_time
                    actions_enregistrees[i] = (key, start_time, duration)
                    print(f"Action mise à jour : {action} avec durée {duration}")

    #else:
        # print(f"La touche {key} n'était pas pressée")

def get_inverse_key(key):
    # Définir les touches opposées
    inverse_keys = {
        Key.up: Key.down,
        Key.down: Key.up,
        Key.left: Key.right,
        Key.right: Key.left,
        # Ajoutez d'autres touches ici si nécessaire
    }
    return inverse_keys.get(key, key)  # Retourne la touche opposée ou la même touche si non trouvée

actions_enregistrees = []
def replay_actions_inverse():
    print("replay_actions_inverse")
    global actions_enregistrees

    # Vérifier si les variables sont initialisées
    if 'actions_enregistrees' not in globals():
        print("Erreur : actions_enregistrees n'est pas initialisé.")
        return

    # Vérifier si actions_enregistrees est une liste
    if not isinstance(actions_enregistrees, list):
        print("Erreur : actions_enregistrees n'est pas une liste.")
        return

    for action in actions_enregistrees:
        if len(action) == 3:
            key, start_time, duration = action
            print(f"Action programmée : {key} pour une durée de {duration} secondes")
            threading.Thread(target=simuler_action, args=[key, duration]).start()

    actions_enregistrees = []  # Réinitialiser la liste d'actions
    print("Rejouer_actions_inverse > Tableau vidé")

def simuler_action(key, duration):
    keyboard_controller.press(key)
    time.sleep(duration)
    keyboard_controller.release(key)

last_click_time = {mouse.Button.left: 0, mouse.Button.middle: 0, mouse.Button.right: 0}
def on_mouse_click(x, y, button, pressed):
    global last_click_time
    current_time = time.time()

    if pressed:
        if current_time - last_click_time[button] < INI_DOUBLE_CLICK_TIMING:
            # Double clic détecté
            handle_double_click(button)
        else:
            # Clic simple
            handle_simple_click(button)
    else:
        # Relâcher la touche si c'est un clic simple
        handle_release_click(button)

    last_click_time[button] = current_time

def handle_double_click(button):
    global absolute_mode
    if button == mouse.Button.left:
        if USE_RELEASE_ALL_KEYS_DOUBLE_CLICK_LEFT: release_all_keys()
        if USE_ABSOLUTE_MODE_DOUBLE_CLICK_LEFT: absolute_mode = True
        press_and_release_after_delay(KEY_DOUBLE_CLICK_LEFT)
    elif button == mouse.Button.middle:
        if USE_RELEASE_ALL_KEYS_DOUBLE_CLICK_MIDDLE: release_all_keys()
        if USE_ABSOLUTE_MODE_DOUBLE_CLICK_MIDDLE: absolute_mode = True
        press_and_release_after_delay(KEY_DOUBLE_CLICK_MIDDLE)
    elif button == mouse.Button.right:
        if USE_RELEASE_ALL_KEYS_DOUBLE_CLICK_RIGHT: release_all_keys()
        if USE_ABSOLUTE_MODE_DOUBLE_CLICK_RIGHT: absolute_mode = True
        press_and_release_after_delay(KEY_DOUBLE_CLICK_RIGHT)

def handle_simple_click(button):
    global absolute_mode
    if button == mouse.Button.left:
        if USE_RELEASE_ALL_KEYS_SIMPLE_CLICK_LEFT: release_all_keys()
        if USE_ABSOLUTE_MODE_SIMPLE_CLICK_LEFT: absolute_mode = True
        press_key(KEY_CLICK_LEFT)
    elif button == mouse.Button.middle:
        if USE_RELEASE_ALL_KEYS_SIMPLE_CLICK_MIDDLE: release_all_keys()
        if USE_ABSOLUTE_MODE_SIMPLE_CLICK_MIDDLE: absolute_mode = True
        press_key(KEY_CLICK_MIDDLE)
    elif button == mouse.Button.right:
        if USE_RELEASE_ALL_KEYS_SIMPLE_CLICK_RIGHT: release_all_keys()
        if USE_ABSOLUTE_MODE_SIMPLE_CLICK_RIGHT: absolute_mode = True
        press_key(KEY_CLICK_RIGHT)

def handle_release_click(button):
    global absolute_mode
    if button == mouse.Button.left:
        if USE_RELEASE_ALL_KEYS_RELEASE_CLICK_LEFT: release_all_keys()
        release_key(KEY_CLICK_LEFT)
        if not USE_ABSOLUTE_MODE_RELEASE_CLICK_LEFT and (USE_ABSOLUTE_MODE_SIMPLE_CLICK_LEFT or USE_ABSOLUTE_MODE_DOUBLE_CLICK_LEFT):
            absolute_mode = False

    elif button == mouse.Button.middle:
        if USE_RELEASE_ALL_KEYS_RELEASE_CLICK_MIDDLE: release_all_keys()
        release_key(KEY_CLICK_MIDDLE)
        if not USE_ABSOLUTE_MODE_RELEASE_CLICK_MIDDLE and (USE_ABSOLUTE_MODE_SIMPLE_CLICK_MIDDLE or USE_ABSOLUTE_MODE_DOUBLE_CLICK_MIDDLE):
            absolute_mode = False

    elif button == mouse.Button.right:
        if USE_RELEASE_ALL_KEYS_RELEASE_CLICK_RIGHT: release_all_keys()
        release_key(KEY_CLICK_RIGHT)
        if not USE_ABSOLUTE_MODE_RELEASE_CLICK_RIGHT and (USE_ABSOLUTE_MODE_SIMPLE_CLICK_RIGHT or USE_ABSOLUTE_MODE_DOUBLE_CLICK_RIGHT):
            absolute_mode = False

def on_mouse_scroll(x, y, dx, dy):
    #print(f"Fonction on_mouse_scroll")
    if dy > 0:
        if USE_RELEASE_ALL_KEYS_SCROLL_UP: release_all_keys()
        press_and_release_after_delay(KEY_SCROLL_UP)
    elif dy < 0:
        if USE_RELEASE_ALL_KEYS_SCROLL_DOWN: release_all_keys()
        press_and_release_after_delay(KEY_SCROLL_DOWN)

def on_mouse_move(x, y):
    global keys_pressed, mouse_moved, absolute_mode
    mouse_moved = True
    KeyUp = Key.up
    KeyDown = Key.down
    if INI_INVERSE_Y:
        KeyUp = Key.down
        KeyDown = Key.up
    # Choix du mode en fonction du mode absolu
    INI_MOVING_MODE = INI_MOVING_MODE_TARGETZOOM if absolute_mode else INI_MOVING_MODE_DEFAULT
    #print(f"on_mouse_move INI_MOVING_MODE {INI_MOVING_MODE} absolute_mode {absolute_mode}")
    # Gestion des touches gauche et droite
    if INI_MOVING_MODE in ["horizontal", "omnidirectional"]:
        if not is_cursor_near_center_x(x):
            if x < centre_x and not keys_pressed.get(Key.left, False):
                press_key(Key.left)
            elif x >= centre_x and keys_pressed.get(Key.left, False):
                release_key(Key.left)

            if x > centre_x and not keys_pressed.get(Key.right, False):
                press_key(Key.right)
            elif x <= centre_x and keys_pressed.get(Key.right, False):
                release_key(Key.right)
        else:
            if keys_pressed.get(Key.left, False):
                release_key(Key.left)
            if keys_pressed.get(Key.right, False):
                release_key(Key.right)

    # Gestion des touches haut et bas
    if INI_MOVING_MODE in ["vertical", "omnidirectional"]:
        if not is_cursor_near_center_y(y):
            if y < centre_y and not keys_pressed.get(KeyUp, False):
                press_key(KeyUp)
            elif y >= centre_y and keys_pressed.get(KeyUp, False):
                release_key(KeyUp)

            if y > centre_y and not keys_pressed.get(KeyDown, False):
                press_key(KeyDown)
            elif y <= centre_y and keys_pressed.get(KeyDown, False):
                release_key(KeyDown)
        else:
            if keys_pressed.get(KeyUp, False):
                release_key(KeyUp)
            if keys_pressed.get(KeyDown, False):
                release_key(KeyDown)

def check_cursor_position():
    #print(f"Fonction check_cursor_position")
    global keys_pressed
    KeyUp = Key.up
    KeyDown = Key.down
    if INI_INVERSE_Y:
        KeyUp = Key.down
        KeyDown = Key.up
    while running:
        x, y = pyautogui.position()

        if is_cursor_near_center_x(x):
            if keys_pressed.get(Key.left, False):  # Vérifier si la touche est pressée avant de la relâcher
                release_key(Key.left)
            if keys_pressed.get(Key.right, False):  # Vérifier si la touche est pressée avant de la relâcher
                release_key(Key.right)

        if is_cursor_near_center_y(y):
            if keys_pressed.get(KeyUp, False):  # Vérifier si la touche est pressée avant de la relâcher
                release_key(KeyUp)
            if keys_pressed.get(KeyDown, False):  # Vérifier si la touche est pressée avant de la relâcher
                release_key(KeyDown)

        time.sleep(INI_REFRESH_CHECK_POSITION)  # Vérification toutes les 100 ms

def on_key_press(key):
    global running
    if key == keyboard.Key.esc:
        running = False

def on_key_release(key):
    global running

def calculate_attraction_force(x, y, force_mode_x='spring', force_mode_y='spring'):
    global absolute_mode
    distance_x = centre_x - x
    distance_y = centre_y - y
    distance = sqrt(distance_x**2 + distance_y**2)
    if distance == 0:
        return 0, 0

    force_constant_x = 0
    force_factor_x = 1
    force_constant_y = 0
    force_factor_y = 1
    if absolute_mode:
        force_constant_x = INI_FORCE_CONSTANT_ABSOLUTE_MODE_X
        force_factor_x = INI_FORCE_FACTOR_ABSOLUTE_MODE_X
        force_constant_y = INI_FORCE_CONSTANT_ABSOLUTE_MODE_Y
        force_factor_y = INI_FORCE_FACTOR_ABSOLUTE_MODE_Y
    else:
        force_constant_x = INI_FORCE_CONSTANT_X
        force_factor_x = INI_FORCE_FACTOR_X
        force_constant_y = INI_FORCE_CONSTANT_Y
        force_factor_y = INI_FORCE_FACTOR_Y

    # Calcul de la force en X
    force_x = (calculate_force_component(distance_x, distance, force_mode_x, x) * force_factor_x) + force_constant_x

    # Calcul de la force en Y
    force_y = (calculate_force_component(distance_y, distance, force_mode_y, y) * force_factor_y) + force_constant_y
    #print(f"Forces force_x {force_x}, force_y {force_y}")
    return force_x, force_y

def calculate_force_component(distance_component, total_distance, force_type, current_position):
    global absolute_mode
    if force_type == 'spring':
        # Force proportionnelle à la distance (ressort)
        return distance_component / total_distance * total_distance
    elif force_type == 'spring':
        # Force proportionnelle à la distance (ressort)
        return distance_component / total_distance * total_distance
    elif force_type == 'friction':
        # Force de frottement
        return -distance_component / total_distance
    elif force_type == 'elastic':
        # Force élastique
        return distance_component
    elif force_type == 'gravitational':
        # Force gravitationnelle
        return distance_component / total_distance**2
    elif force_type == 'tension':
        # Force de tension
        if absolute_mode:
            if total_distance > (tolerance_absolute_x+tolerance_absolute_y)/2:
                return distance_component
            else:
                return 0
        else:
            if total_distance > (tolerance_absolute_x+tolerance_absolute_y)/2:
                return distance_component
            else:
                return 0
    elif force_type == 'null':
        # Aucune force - conserve la position actuelle
        return 0
    elif force_type == 'positive':
        # Force "positive" - conserve la position actuelle si supérieure à zéro
        if current_position > 0:
            return 0  # Pas de changement
        else:
            return distance_component  # Applique la force normalement
    else:
        # Aucune force
        return 0


def start_mouse_control():
    global running, absolute_mode
    print("Starting mouse control.")

    mouse_listener = mouse.Listener(on_click=on_mouse_click, on_move=on_mouse_move, on_scroll=on_mouse_scroll)
    key_listener = keyboard.Listener(on_press=on_key_press)

    mouse_listener.start()
    key_listener.start()

    cursor_check_thread = threading.Thread(target=check_cursor_position)
    cursor_check_thread.start()

    while running:
        mouse_x, mouse_y = pyautogui.position()
        if not absolute_mode:
            force_x, force_y = calculate_attraction_force(mouse_x, mouse_y, INI_FORCE_TYPE_DEFAULT_MODE_X, INI_FORCE_TYPE_DEFAULT_MODE_Y)
        else:
            force_x, force_y = calculate_attraction_force(mouse_x, mouse_y, INI_FORCE_TYPE_ABSOLUTE_MODE_X, INI_FORCE_TYPE_ABSOLUTE_MODE_Y)
        pyautogui.moveRel(force_x, force_y)
        time.sleep(INI_REFRESH_FORCE_CALCUL)

    mouse_listener.stop()
    key_listener.stop()
    cursor_check_thread.join()

def set_globals_from_ini(config):
    for section in config.sections():
        for key, value in config.items(section):
            # Suppression des guillemets pour les chaînes de caractères
            if value.startswith(("'", '"')) and value.endswith(("'", '"')):
                value = value[1:-1]
            # Conversion en entier, flottant ou booléen si nécessaire
            elif value.isdigit():
                value = int(value)
            elif value.replace('.', '', 1).isdigit():
                value = float(value)
            elif value.lower() in ['true', 'false']:
                value = True if value.lower() == 'true' else False

            # Création d'une variable globale pour chaque clé trouvée dans le fichier INI
            globals()[key.upper()] = value
            logging.info(f"{key.upper()} = {repr(globals()[key.upper()])}")

def main():
    check_if_already_running()

    # Récupération des arguments de la ligne de commande
    game, system = extract_game_and_system(sys.argv)

    if not game or not system:
        print("Erreur : Paramètres 'game' et 'system' manquants.")
        sys.exit(1)

    print(f"Lancement du script pour le jeu '{game}' sur le système '{system}'.")

    # Chargement de la configuration
    config = load_config_mapper(system, game)
    if config is None:
        print("Erreur lors du chargement de la configuration.")
        sys.exit(1)
    set_globals_from_ini(config)

    # Affichage de bienvenue
    print(">> GunRPointer - Control FPS with Pointer HID")
    print("Press ESC to exit")

    # Initialisation du contrôle de la souris et du clavier
    initialize_mouse_and_keyboard_control()
    start_mouse_control()

if __name__ == "__main__":
    main()
