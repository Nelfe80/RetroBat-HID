import hid
import subprocess
import json
import configparser
import os

def get_hid_paths():
    all_devices = hid.enumerate()
    hid_paths = {f"HID\\VID_{device['vendor_id']:04X}&PID_{device['product_id']:04X}": bytes.decode(device['path']).replace('\\\\', '\\') for device in all_devices}
    print("HID Paths from hid.enumerate():")
    for key, value in hid_paths.items():
        print(f"{key} -> {value}")
    return hid_paths

def find_matching_hidpath(device_id, hid_paths):
    simplified_device_id = device_id.replace('\\', '&').split('&')
    for hid_id, path in hid_paths.items():
        for segment in simplified_device_id:
            if segment in hid_id:
                corrected_path = path.replace('\\\\', '\\')  # Ensure correct path format
                if not corrected_path.startswith('\\\\?\\'):
                    corrected_path = '\\\\?' + corrected_path
                return corrected_path
    return 'Unknown'

def get_mouse_hid_devices():
    ps_script = """
    Get-PnpDevice |
    Where-Object {($_.Class -eq 'Mouse' -or $_.Class -eq 'HIDClass') -and $_.Service -eq 'mouhid' -and $_.Status -eq 'OK'} |
    Select-Object DeviceID, FriendlyName, Manufacturer, DriverVersion |
    ConvertTo-Json
    """
    result = subprocess.run(["powershell", "-Command", ps_script], capture_output=True)
    output = result.stdout.decode(errors='ignore')
    mouse_devices = json.loads(output)
    print("Mouse Devices from PowerShell:")
    for device in mouse_devices:
        print(f"{device['DeviceID']} -> {device}")
    return mouse_devices

def save_hid_devices_to_ini(mouse_devices, hid_paths, ini_path='HIDsget.ini'):
    config = configparser.ConfigParser()
    if not os.path.exists(ini_path):
        open(ini_path, 'w').close()
    config.read(ini_path)

    for device in mouse_devices:
        device_id = device.get('DeviceID', 'Unknown')
        section_name = device_id.replace("\\", "_").replace("&", "_")
        hidpath = find_matching_hidpath(device_id, hid_paths)
        print(f"Matching HID path for {device_id}: {hidpath}")

        config[section_name] = {
            'DeviceID': device_id,
            'FriendlyName': str(device.get('FriendlyName', 'Unknown')),
            'Manufacturer': str(device.get('Manufacturer', 'Unknown')),
            'DriverVersion': str(device.get('DriverVersion', 'Unknown')),
            'HIDPath': hidpath
        }

    with open(ini_path, 'w') as configfile:
        config.write(configfile)

hid_paths = get_hid_paths()
mouse_devices = get_mouse_hid_devices()
save_hid_devices_to_ini(mouse_devices, hid_paths)
