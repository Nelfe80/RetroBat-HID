import configparser
import re

def condition_met(config_lines, section, condition):
    if condition:
        section_header = f"[{section}]"
        section_found = False
        for line in config_lines:
            if line.strip().lower() == section_header.lower():
                section_found = True
            elif line.strip().startswith('[') and section_found:
                # Si une nouvelle section commence, arrête la recherche
                break
            elif section_found and condition in line:
                return True
        return False
    return True

def update_target_config(file_path, section, key, new_value):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    section_found = False
    key_found = False
    for i, line in enumerate(lines):
        if line.strip().lower() in [f"{section.lower()}", f";{section.lower()}"]:
            section_found = True
        if section_found and line.strip().startswith(f"{key} ="):
            lines[i] = f"{key} = {new_value}\n"
            key_found = True
            break

    if not key_found and section_found:
        lines.append(f"{key} = {new_value}\n")

    with open(file_path, 'w') as file:
        file.writelines(lines)

def process_instruction(line):
    print(f"Traitement de la ligne : {line}")
    pattern = r"file_source:'(.+?)' section_source:'(.+?)' field_source:'(.+?)'(?: if_source:'(.+?)')? file_target:'(.+?)' section_target:'(.+?)' field_target:'(.+?)'"
    match = re.match(pattern, line)

    if match:
        file_source, section_source, field_source, if_source, file_target, section_target, field_target = match.groups()
        print(f"Source : {file_source}, Section Source : {section_source}, Champ Source : {field_source}, Condition Source : {if_source}")
        print(f"Cible : {file_target}, Section Cible : {section_target}, Champ Cible : {field_target}")

        with open(file_source, 'r') as f:
            source_lines = f.readlines()

        if condition_met(source_lines, section_source, if_source):
            value = None
            for line in source_lines:
                if line.strip().startswith(f"{field_source} ="):
                    value = line.split('=')[1].strip()
                    break

            if value:
                update_target_config(file_target, section_target, field_target, value)
                print(f"Valeur {value} écrite dans {section_target}[{field_target}] du fichier cible")
            else:
                print("Valeur non trouvée, aucune écriture dans le fichier cible.")
        else:
            print("La condition spécifiée n'est pas remplie. Aucune action effectuée.")
    else:
        print(f"Impossible d'analyser la ligne : {line}")

def execute_instructions_from_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            process_instruction(line.strip())

run_file = 'getput.run'
execute_instructions_from_file(run_file)
