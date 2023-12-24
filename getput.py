import configparser
import re

def process_instruction(line):
    # Utiliser une expression régulière pour extraire les informations
    pattern = r"file_source:'(.+)' field_source:'(.+)' file_target:'(.+)' field_target:'(.+)'"
    match = re.match(pattern, line)

    if match:
        file_source, field_source, file_target, field_target = match.groups()

        # Lire la source
        config_source = configparser.ConfigParser()
        config_source.read(file_source)
        value = config_source.get('DEFAULT', field_source)  # Assumer que le champ est dans la section 'DEFAULT'

        # Écrire dans la cible
        config_target = configparser.ConfigParser()
        config_target.read(file_target)
        if not config_target.has_section('DEFAULT'):
            config_target.add_section('DEFAULT')
        config_target.set('DEFAULT', field_target, value)
        with open(file_target, 'w') as target_file:
            config_target.write(target_file)

def execute_instructions_from_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            process_instruction(line.strip())

# Chemin du fichier getput.run
run_file = 'getput.run'

# Exécution des instructions
execute_instructions_from_file(run_file)
