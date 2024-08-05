# The following is used to optain the power measurment for 1 tapo 

import os
import signal
import subprocess
import sys
import asyncio
from datetime import datetime
from tapo import ApiClient, EnergyDataInterval
import argparse
import time



LOG_DIR = ".../PowerGuard/code/logs/log_power"  # Directory where logs will be stored

def log_to_file(message, device):
    
    """
    Append a message to a device-specific log file. Creates the log file if it doesn't exist.

    Args:
        message (str): Message to write to the log file.
        device (str): Device identifier or name to use for the log file name.
    """
    
    log_filename = f"{device}.log"
    log_path = os.path.join(LOG_DIR, log_filename)

    # Check if the log file exists
    if not os.path.exists(log_path):
        # Create a new log file if it doesn't exist
        with open(log_path, 'w') as new_log_file:
            new_log_file.write(f"Log file for {device}\n")

    # Append the message to the log file
    with open(log_path, 'a') as log_file:
        log_file.write(message)


# edit the dictionary to include your lab setup. i.e 
devtapo = {
       "device_name": "tapo_id",      # example-> "humidifier":"tapo1"
       
    }

def get_ip(deviceid):

    """
    Function to return an IP address given a device name.
    It reads the devices.txt file and obtains the MAC address of the device.
    It then obtains the IP address after running an ARP query.

    Args:
        deviceid: Name of the device. This should correspond to the device identifier in the devices.txt file.
    Returns:
        ip_address: The IP address corresponding to the device.
    """

    # May change device file to user argument
    DEVICE_FILE = ".../opt/moniotr/etc/devices.txt"   #Ensure that the path is correct.
    ip_address = ""   # do not edit

    # Open file and read devices
    with open(DEVICE_FILE) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            print(line)
            if not line:
                continue
            parts = line.split()
            mac = parts[0].strip()
            name = parts[1].strip()
            if name == deviceid:
                try:
                    arp = subprocess.Popen(["arp"], stdout=subprocess.PIPE)
                    out = subprocess.check_output(["grep", mac], stdin=arp.stdout)
                    ip_address = out.decode().split()[0].strip()
                except Exception as e:
                    print("Error running ARP:", e)
        print(ip_address)
        return ip_address



async def main():


    parser = argparse.ArgumentParser(description="Tapo API Example")
    parser.add_argument("--d", "--device", type=str, dest="device", help="device used (i.e smartbulb)")
    
    # Uncomment the following if you wish to input the tapo id, username and password from commandline
    #parser.add_argument("--u", "--username", type=str, dest="username", help="Tapo username")
    #parser.add_argument("--p", "--password", type=str, dest="password", help="Tapo password")
    #parser.add_argument("--id", "--device_id", type=str, dest="device_id", help="Tapo device ID")
    
    args = parser.parse_args()

    dev           = str(args.device)
    tapo_username = <username>
    tapo_password = <password>
    tapoid        = devtapo[dev]
    ip_address    = get_ip(tapoid)
    freq          = 1  # edit the frequency 

    client = ApiClient(tapo_username, tapo_password)
    device = await client.p110(ip_address)

    device_info = await device.get_device_info()
    #print(f"Device info: {device_info.to_dict()}")

    device_usage = await device.get_energy_usage()
    #print(f"Device usage: {device_usage.to_dict()['current_power']}")
    log_entries = []
    while True:
        device_usage = await device.get_energy_usage()
        current_power = await device.get_current_power()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(int(freq))
        log_msg = f"[{timestamp}, {device_usage.to_dict()['current_power']}]"
        #log_entries.append(log_msg)
        log_to_file(str(log_msg),dev)    #log_entries))


if __name__ == "__main__":
    asyncio.run(main())
