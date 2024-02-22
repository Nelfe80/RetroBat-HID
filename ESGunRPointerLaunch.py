import sys
import os
import requests
import urllib.parse
import configparser
import subprocess
import shlex
import logging

logging.basicConfig(level=logging.INFO)

def find_ini_file(start_path):
    current_path = start_path
    while current_path != os.path.dirname(current_path):
        ini_path = os.path.join(current_path, 'plugins', 'GunRPointer', 'config.ini')
        if os.path.exists(ini_path):
            return ini_path
        current_path = os.path.dirname(current_path)
    raise FileNotFoundError("Le fichier events.ini n'a pas été trouvé.")

def load_config():
    current_working_dir = os.getcwd()
    config_path = find_ini_file(current_working_dir)
    config = configparser.ConfigParser()
    config.read(config_path)
    return config



def execute_command(event, params):
    creation_flags = subprocess.CREATE_NO_WINDOW
    gun_r_pointer_path = config['Settings']['GunRPointerPath']
    command_template = config['Settings']['GunRPointerCommand']
    roms_path = config['Settings']['RomsPath']
    game = params.get('param2', '')
    logging.info(f"game: {game}")
    system = params['param1'].replace(roms_path, '').split('\\')[0]
    logging.info(f"system: {system}")
    command = command_template.format(
        GunRPointerPath=gun_r_pointer_path,
        game=game,
        system=system
    )
    logging.info(f"Executing the command : {command}")
    subprocess.Popen(command, shell=True, creationflags=creation_flags)
    #subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=creation_flags)

def get_current_directory_event():
    return os.path.basename(os.getcwd())

def get_command_line():
    pid = os.getpid()
    command = f'wmic process where ProcessId={pid} get CommandLine'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if error:
        logging.info(f"Error: {error.decode('cp1252').strip()}")
        #input("Appuyez sur Entrée pour continuer...")
        return ""
    try:
        return output.decode('utf-8').strip()
    except UnicodeDecodeError:
        return output.decode('cp1252').strip()

def clean_and_split_arguments(command_line):
    command_line = command_line.replace('""', '"')
    try:
        arguments = shlex.split(command_line)
    except ValueError as e:
        logging.info(f"Erreur lors du découpage des arguments: {e}")
        arguments = []
    if arguments:
        arguments = arguments[2:]
    return arguments

if __name__ == "__main__":
    config = load_config()
    event = get_current_directory_event()
    command_line = get_command_line()
    logging.info(f"command_line: {command_line}")
    arguments = clean_and_split_arguments(command_line)
    params = {f'param{i}': arg for i, arg in enumerate(arguments, start=1)}
    logging.info(f"arguments: {arguments}")
    logging.info(f"params: {params}")
    #input("Appuyez sur Entrée pour continuer...")
    execute_command(event, params)
