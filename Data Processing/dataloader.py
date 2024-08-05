# The following libraries are used for all the functions
# They are prerequisites for the use of the code.
import numpy as np 
import pathlib 
import os
import re
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from sklearn.metrics import confusion_matrix
from sklearn.metrics import r2_score
import time
from time import sleep
import subprocess
import signal
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pandas as pd
from datetime import datetime
import matplotlib as mpl



def loadPow(dev):

     directory = f"...\results_sequence\power\{dev}"
     pow_hm = {}
     #      for directory in os.scandir(pow_dir):
     #           device = directory.name
     # Load the numpy file
     for path in os.scandir(pathlib.Path(directory)):

          filepath = os.path.join(directory, path)

          values = np.load(filepath)

          filename = os.path.basename(path)

        #   # Remove the extension to get the device name
          device = os.path.splitext(filename)[0]

        #   # Convert the loaded numpy array to a string
          data_str = str(values)

          # Use regular expressions to find all timestamp-value pairs
          pairs = re.findall(r"\['(.*?)', (\d+)\]", data_str)

          # Initialize a list to store formatted timestamp-value pairs
          formatted_data = []

          # Process each pair and append it to the formatted_data list
          for pair in pairs:
               timestamp, value = pair
               formatted_data.append([timestamp, int(value)])

          pow_hm[device] = formatted_data

     return pow_hm



def loadPowTest(day)

     directory = f"...\results_week\power\{day}"
     pow_hm = {}
     #      for directory in os.scandir(pow_dir):
     #           device = directory.name
     # Load the numpy file
     for path in os.scandir(pathlib.Path(directory)):

          filepath = os.path.join(directory, path)

          values = np.load(filepath)

          filename = os.path.basename(path)

        #   # Remove the extension to get the device name
          device = os.path.splitext(filename)[0]

        #   # Convert the loaded numpy array to a string
          data_str = str(values)

          # Use regular expressions to find all timestamp-value pairs
          pairs = re.findall(r"\['(.*?)', (\d+)\]", data_str)

          # Initialize a list to store formatted timestamp-value pairs
          formatted_data = []

          # Process each pair and append it to the formatted_data list
          for pair in pairs:
               timestamp, value = pair
               formatted_data.append([timestamp, int(value)])

          pow_hm[device] = formatted_data

     return pow_hm


def loadNetTest(day):

     directory = f"...\results_week\network\{day}"
     net_hm = {}

     for path in os.scandir(pathlib.Path(directory)):

          device = os.path.basename(path)

          with open(path, 'r') as file:
               lines = file.readlines()
          entries = [line.strip().split() for line in lines]

          # Combine date and time fields and convert to datetime object
          entries = [[str(f"{entry[0]} {entry[1]}"), int(entry[2])] for entry in entries]
 
          net_hm[device] = entries


     return net_hm



def loadNet(dev):

     directory = f"...\results_sequence\network\{dev}"
     net_hm = {}

     for path in os.scandir(pathlib.Path(directory)):

          device = os.path.basename(path)

          with open(path, 'r') as file:
               lines = file.readlines()
          entries = [line.strip().split() for line in lines]

          # Combine date and time fields and convert to datetime object
          entries = [[str(f"{entry[0]} {entry[1]}"), int(entry[2])] for entry in entries]

          net_hm[device] = entries


     return net_hm

def loadLog(dev):

     log_file = f"...\results_sequence\log\{dev}"

     # Define column names
     columns = ['Start Time', 'End Time', 'State', 'Device']

     # Read the log file into a DataFrame
     df = pd.read_csv(log_file, delimiter='|', skipinitialspace=True, parse_dates=['Start Time', 'End Time'], names=columns)

     return df[2:]

def loadLogTest(day):

     log_file = f"...\results_week\log\{day}"

     # Define column names
     columns = ['Start Time', 'End Time', 'State', 'Device']

     # Read the log file into a DataFrame
     df = pd.read_csv(log_file, delimiter='|', skipinitialspace=True, parse_dates=['Start Time', 'End Time'], names=columns)
     # note, that the first two rows were the header along with the seperator lines.
     return df[2:]



