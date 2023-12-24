import configparser
import re

def condition_met(config, section, condition):
    if condition:
        key, value = [x.strip() for x in condition.split('=')]
        return config.get(section, key, fallback=None) == value
    return True

def process_instruction(line):
    pattern = r"file_source:'(.+)' section_source:'(.+)' field_source:'(.+)'(?: if_source:'(.+)')? file_target:'(.+)' section_target:'(.+)' field_target:'(.+)'"
    match = re.match(pattern, line)

    if match:
        file_source, section_source, field_source, if_source, file_target, section_target, field_target = match.groups()

        # Lire la source
        config_source = configparser.ConfigParser()
        config_source.read(file_source)

        if condition_met(config_source, section_source, if_source):
            value = config_source.get(section_source, field_source, fallback=None)

            # Écrire dans la cible
            if value is not None:
                config_target = configparser.ConfigParser()
                config_target.read(file_target)
                if not config_target.has_section(section_target):
                    config_target.add_section(section_target)
                config_target.set(section_target, field_target, value)
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
