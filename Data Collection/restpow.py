import os
import signal
import subprocess
import sys
import asyncio
from datetime import datetime
from tapo import ApiClient, EnergyDataInterval
import argparse
import time

devtapo = {
       "device_name":"tapo_id",
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
    DEVICE_FILE = ".../opt/moniotr/etc/devices.txt" # ensure right path
    ip_address = "" #leave empty

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

    parser = argparse.ArgumentParser(description="The following program is used to obtain the power measurments")
    parser.add_argument("--d", "--device", type=str, dest="device", help="device used (i.e smartbulb)")

    args           =  parser.parse_args()
    dev            =  str(args.device)
    tapo_username  =  <username>
    tapo_password  =  <password>
    ip_address     =  get_ip(devtapo[dev])

    client = ApiClient(tapo_username, tapo_password)
    device = await client.p110(ip_address)


    await device.off()

    # Change the delay from 60 to your requirements
    await asyncio.sleep(60)

    await device.on()


if __name__ == "__main__":
    asyncio.run(main())
