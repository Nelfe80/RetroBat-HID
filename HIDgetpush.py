import pywinusb.hid as hid
import configparser
import os

def get_hid_devices():
    # Créer un objet ConfigParser
    config = configparser.ConfigParser()

    # Trouver tous les périphériques HID
    all_devices = hid.find_all_hid_devices()

    # Parcourir et enregistrer les détails des périphériques HID
    for index, device in enumerate(all_devices):
        config[f'Device_{index}'] = {
            'VendorID': hex(device.vendor_id),
            'ProductID': hex(device.product_id),
            'SerialNumber': device.serial_number,
            'HIDPath': device.device_path
        }

    # Écrire dans un fichier INI
    with open('HIDsget.ini', 'w') as configfile:
        config.write(configfile)

# Appeler la fonction
get_hid_devices()
