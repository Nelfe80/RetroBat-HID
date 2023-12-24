import pywinusb.hid as hid
import configparser
import os

def get_hid_devices():
    # Chemin du fichier INI
    ini_path = 'HIDsget.ini'

    # Créer un objet ConfigParser
    config = configparser.ConfigParser()

    # Vérifier si le fichier INI existe déjà
    if not os.path.exists(ini_path):
        open(ini_path, 'w').close()

    # Lire le fichier INI existant
    config.read(ini_path)

    # Trouver tous les périphériques HID
    all_devices = hid.find_all_hid_devices()

    # Parcourir et enregistrer les détails des périphériques HID
    for index, device in enumerate(all_devices):
        section_name = f'Device_{index}'
        config[section_name] = {
            'VendorID': hex(device.vendor_id),
            'ProductID': hex(device.product_id),
            'SerialNumber': device.serial_number or 'None',
            'HIDPath': device.device_path
        }

    # Écrire dans le fichier INI
    with open(ini_path, 'w') as configfile:
        config.write(configfile)

# Appeler la fonction
get_hid_devices()
