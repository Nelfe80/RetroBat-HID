import re

def read_ini_field(file_path, field):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(field):
                return line.split('=')[1].strip()
    return None

def write_ini_field(file_path, field, value):
    lines = []
    found = False
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(field):
                lines.append(f'{field}={value}\n')
                found = True
            else:
                lines.append(line)

    if not found:
        lines.append(f'{field}={value}\n')

    with open(file_path, 'w') as file:
        file.writelines(lines)

def process_instruction(line):
    pattern = r"file_source:'(.+)' field_source:'(.+)' file_target:'(.+)' field_target:'(.+)'"
    match = re.match(pattern, line)

    if match:
        file_source, field_source, file_target, field_target = match.groups()

        # Lire la valeur du champ source
        value = read_ini_field(file_source, field_source)

        # Écrire la valeur dans le champ cible
        if value is not None:
            write_ini_field(file_target, field_target, value)

def execute_instructions_from_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            process_instruction(line.strip())

# Chemin du fichier getput.run
run_file = 'getput.run'

# Exécution des instructions
execute_instructions_from_file(run_file)
