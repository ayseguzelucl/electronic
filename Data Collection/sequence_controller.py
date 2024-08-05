import subprocess
from datetime import datetime
from time import sleep
import os
import time
import signal
import random



def initLog(timestamp):
    """
    Initialize a log file with a given timestamp.

    Args:
        timestamp (str): Timestamp string to be used in the log file name.

    Returns:
        str: Path to the created log file.
    """
    log_dir = ".../PowerGuard/code/logs/log_activities"  # Directory where logs will be stored (adjust as needed)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_filename = f"{timestamp}"  # Example log file name format
    log_path = os.path.join(log_dir, log_filename)

    # Create or open the log file
    with open(log_path, "w") as log_file:
        # Write initial header to the log file
        log_file.write("     Start Time     |      End Time       |  State   |    Device     \n")
        log_file.write("--------------------|---------------------|----------|---------------\n")

    return log_path



def log_to_file(message,log_file):

    with open(log_file, 'a') as log_file:
        log_file.write(message)


def getMac(device):
    devices = {
     'device_name' :'mac address',
     ...
    }
    return devices[device]


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



def getIp(mac):

   command = f"ip neighbor | grep -i {fix_mac_address(mac)} | cut -d' ' -f1"

   # Execute the command and capture the output
   output = subprocess.check_output(command, shell=True)

   # Decode the output and store the IP address in a variable
   ip_address = output.decode("utf-8").strip()

   return ip_address


def createInstruction(device,duration):

    instructions = {
        "<Device>":f"<device>; <tapo_id>; <wifi>; <mac_address>; <phone_id>; <app package>; <init wait>; <1st tap coords>; <delay>s; <2nd tap coords>;\n"
       "example": f"example;tapoN;iot_testbed_N;NN:NN:NN:NN:NN:NN;pixelN;package.library;(initial wait)s;tap N N;{duration}s;tap N N\n",

    }

    file_path = f".../PowerGuard/code/logs/log_instructions/{device}"

    # Open the file in write mode ('w')
    with open(file_path, 'w') as file:
        # Write the string to the file
        file.write(instructions[device])

def triggerAct(device,duration):
    path = ".../PowerGuard/code/trigger_activities.sh"
    # The following controlls the activations.
    if device == "Exception":
          """
             In case any devices require further steps i.e voice recognition
             enter those instructions in if statements here.
             
          """
    else:
           createInstruction(device,duration)
           config_fpath = device
           subprocess.run(["sudo", "bash", path, "--config_fpath", config_fpath,"&"])



# log file initialized here
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_file = initLog(timestamp)

def stateMachine(device,mac,ip,state,signal):
   """
    The following is a state machine which controls the order of the experiments.
    it is used to ensure that the activities do not overlap.

    args:
         device, mac, ip (of target device)
         signals: "start", "continue", "end"
   """
   # initializations and constants
   duration = 60           #adjust as needed
   # create log file for the attacks
   # this is its header
   if state == 0:
      if signal == "start":
         subprocess.run(["nohup","sudo","python3","getpow.py","--d",device,"&"])
         subprocess.run(["sudo", "/opt/moniotr/bin/tag-experiment", "start", mac,device])
         createInstruction(device,duration)
         return 1
      if signal == "continue":
          subprocess.run(["nohup","sudo","python3","restpow.py","--d",device,"&"])
          sleep(60) #if not enough increase amount.
          return 1
      if signal == "end":
         subprocess.run(["sudo","pkill","-f","getpow.py"])
         subprocess.run(["sudo", "/opt/moniotr/bin/tag-experiment", "stop", mac,device])
         return -1

   if state == 1:
      # This is the idle state
      time_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      time.sleep(duration)
      time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      log_to_file(f"{time_start} | {time_end} |   idle   | {device}\n",log_file)
      return 2

   if state == 2:
      # this is the activity state
      time_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      triggerAct(device,duration)
      time.sleep(duration)
      time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      log_to_file(f"{time_start} | {time_end} |  activt  | {device}\n",log_file)
      return 3

   if state == 3:
     # idle with attack
     time_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     subprocess.run(["sudo", "hping3", "-c", "12000", "-d", "120", "-S", "-w", "64", "-p", "80", "--flood", "--rand-source", ip,"&"])
     # Sleep for some time or do other tasks
     time.sleep(duration)
     # Wait for the subprocess to terminate
     subprocess.run(["sudo","pkill","-f","hping3"])
     time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     log_to_file(f"{time_start} | {time_end} | idle_attk | {device}\n",log_file)
     return 4

   if state == 4:
     # acrivity with flood attack

     time_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     triggerAct(device,duration)
     subprocess.run(["sudo", "hping3", "-c", "12000", "-d", "120", "-S", "-w", "64", "-p", "80", "--flood", "--rand-source", ip, "&"])
     time.sleep(duration)
     subprocess.run(["sudo","pkill","-9","hping3"])
     time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     log_to_file(f"{time_start} | {time_end} | actv_attk | {device}\n",log_file)
     subprocess.run(["sudo","pkill","-9","hping3"])
     return 0


# Select device and number of repetitions
# Also initialize the state
device         = <device>
repetitions    = reps * 5  # There are 5 stages in the  state machine. Hence change 1 to the number of repetitions desired.
curState       = 0      #Dont change

# The mac and ip are automatecaly extracted
mac            = getMac(device)
ip             = getIp(mac)

# Initialize the state machine
# This will create the relevant pcap files, and begin power capture
try:

   curState = stateMachine(device,mac,ip,curState,"start")

   # Then begin loop to repeat sequence based on desired number of repetitions
   for i in range(repetitions):
      nextState = stateMachine(device,mac,ip,curState,"continue")
      curState  = nextState
      print(curState)
except Exception as e:
    print(f"Error occurred: {e}")
finally:
    _ = stateMachine(device,mac,ip,0,"stop")
# Once the repetitions are completed the following will terminate the processes and
# generate the files in the log_power, and pcap files.
_ = stateMachine(device,mac,ip,0,"stop")


