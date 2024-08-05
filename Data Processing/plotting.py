# The following libraries are used for all the functions
# They are prerequisites for the use of the code.
import numpy as np 
import pathlib 
import os
import re
from datetime import datetime
import pandas as pd
import time
from time import sleep
import subprocess
import signal
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib as mpl
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn import svm
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from sklearn.metrics import confusion_matrix
import statistics
from sklearn import svm
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
import warnings
# Ignore specific warning by category
warnings.filterwarnings('ignore')


#   The following are data loading and formating functions for the Power, Network and log files.


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



def makePlots(device, pow_hm, net_hm, log_hm):

    """
      Description:

         The following function generates the timeseries plot, indicating the power, the network or both signals together
         along with the regions of their states. The function determines automatecally which ones are passed, hence 
         to plot only one of the two signals, leave the other argument as "_"

      Input args:

         device, power, network, activity log
    """


    if (len(pow_hm) > 0) and (len(net_hm) > 0):
        both = 1
        timestamps1, values1 = zip(*pow_hm[device])
        timestamps2, values2 = zip(*net_hm[device])
    elif (len(net_hm) > 0) and (len(pow_hm) == 0):
        both = 0
        timestamps, values = zip(*net_hm[device])
    else:
        both = 0
        timestamps, values = zip(*pow_hm[device])

    if both == 1:
        # Convert timestamps to datetime objects
        timestamps1 = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in timestamps1]
        timestamps2 = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in timestamps2]

        # Calculate the time differences in minutes from the first timestamp
        start_time = min(timestamps1[0], timestamps2[0])
        time_diffs1 = [(ts - start_time).total_seconds() / 60 for ts in timestamps1]
        time_diffs2 = [(ts - start_time).total_seconds() / 60 for ts in timestamps2]

        # Plot
        fig, ax1 = plt.subplots(figsize=(16, 3))

        # Plot power on the primary y-axis
        ax1.plot(time_diffs1, values1, marker='.', label=f"{device} Power", color="blue")
        ax1.set_xlabel("Time (minutes)")
        ax1.set_ylabel("Power (mWh)", color="blue")
        ax1.tick_params(axis='y', labelcolor="blue")

        # Create secondary y-axis and plot network traffic
        ax2 = ax1.twinx()
        ax2.plot(time_diffs2, values2, marker='.', label=f"{device} Network Traffic", color="red")
        ax2.set_ylabel("Network Traffic (Bytes)", color="red")
        ax2.tick_params(axis='y', labelcolor="red")

        # Convert 'Start Time' and 'End Time' to datetime objects
        log_hm['Start Time'] = pd.to_datetime(log_hm['Start Time'], format="%Y-%m-%d %H:%M:%S")
        log_hm['End Time'] = pd.to_datetime(log_hm['End Time'], format="%Y-%m-%d %H:%M:%S")

        # Plot highlighted regions for device states
        device_df = log_hm[log_hm['Device'] == device]
        state_labels = {'idle': 'Idle', 'idle_atk': 'Idle with Attack', 'activt': 'Active', 'actv_atk': 'Active with Attack'}
        state_colors = {'idle': 'blue', 'idle_atk': 'green', 'activt': 'red', 'actv_atk': 'orange'}
        state_legend = {}

        lst_state = device_df['State'].unique()
        lst_state = lst_state[:-1]

        for state in lst_state:
            state_df = device_df[device_df['State'] == state]
            state_legend[state.strip()] = state_labels[state.strip()]
            for index, row in state_df.iterrows():
                start_diff = (row['Start Time'] - start_time).total_seconds() / 60
                end_diff = (row['End Time'] - start_time).total_seconds() / 60
                ax1.axvspan(start_diff, end_diff, alpha=0.3, color=state_colors[state.strip()])

        # Format x-axis to show time in minutes
        ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.0f}'))

        # Set x-axis limits to start from 0 and show a range, e.g., 120 minutes
        ax1.set_xlim(0, 120)

        # Generate legend using stored legend labels and colors
        legend_labels = list(state_legend.values())
        legend_handles = [plt.Rectangle((0, 0), 1, 1, color=state_colors[state.strip()], alpha=0.3) for state in state_legend]
        mpl.rcParams['font.size'] = 14  # Set the font size
        ax1.legend(legend_handles, legend_labels, loc='upper center', bbox_to_anchor=(0.425, 1.3), ncol=4, fontsize=13)
        ax1.grid(True)
        plt.savefig(rf'...\{device}_both.pdf', bbox_inches='tight', format='pdf')
        plt.show()

    else:
        # Convert timestamps to datetime objects
        timestamps = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in timestamps]

        # Calculate the time differences in minutes from the first timestamp
        start_time = timestamps[0]
        time_diffs = [(ts - start_time).total_seconds() / 60 for ts in timestamps]

        # Plot
        plt.figure(figsize=(8, 3))

        # Plot network traffic or power depending on the available data
        plt.plot(time_diffs, values, marker='.', label=f"{device} {'Network Traffic' if len(net_hm) > 0 else 'Power'}", color="0.3")
        plt.xlabel("Time (minutes)")
        plt.ylabel("Network Traffic (Bytes)" if len(net_hm) > 0 else "Power (mWh)")

        # Convert 'Start Time' and 'End Time' to datetime objects
        log_hm['Start Time'] = pd.to_datetime(log_hm['Start Time'], format="%Y-%m-%d %H:%M:%S")
        log_hm['End Time'] = pd.to_datetime(log_hm['End Time'], format="%Y-%m-%d %H:%M:%S")

        # Plot highlighted regions for device states
        device_df = log_hm[log_hm['Device'] == device]
        state_labels = {'idle': 'Idle', 'idle_atk': 'Idle with Attack', 'activt': 'Active', 'actv_atk': 'Active with Attack'}
        state_colors = {'idle': 'blue', 'idle_atk': 'green', 'activt': 'red', 'actv_atk': 'orange'}
        state_legend = {}

        lst_state = device_df['State'].unique()
        lst_state = lst_state[:-1]

        for state in lst_state:
            state_df = device_df[device_df['State'] == state]
            state_legend[state.strip()] = state_labels[state.strip()]
            for index, row in state_df.iterrows():
                start_diff = (row['Start Time'] - start_time).total_seconds() / 60
                end_diff = (row['End Time'] - start_time).total_seconds() / 60
                plt.axvspan(start_diff, end_diff, alpha=0.3, color=state_colors[state.strip()])

        # Format x-axis to show time in minutes
        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.0f}'))

        # Set x-axis limits to start from 0 and show a range, e.g., 120 minutes
        plt.xlim(0, 120)

        # Generate legend using stored legend labels and colors
        legend_labels = list(state_legend.values())
        legend_handles = [plt.Rectangle((0, 0), 1, 1, color=state_colors[state.strip()], alpha=0.3) for state in state_legend]
        mpl.rcParams['font.size'] = 14  # Set the font size
        plt.legend(legend_handles, legend_labels, loc='upper center', bbox_to_anchor=(0.425, 1.3), ncol=4, fontsize=13)
        plt.grid(True)
        plt.savefig(f'...\figures\{device}_net.pdf' if len(net_hm) > 0 else f'...\figures\{device}_power.pdf', bbox_inches='tight', format='pdf')
        plt.show()





def ensure_every_second_has_value(timestamps_values):

    """

      Description:

         Due to the discovery that the TP Tapo P110 true time period is 1.06 seconds instead of 1, some time instances do not have
         a reading. Also when the network traffic is 0, it is not shown along a timestamp. This function allows the user to fill in the
         missing timestamps (values are 0).

      Input arg:

         timeseries ([[timestamp,value],..]

    """

    if not timestamps_values:
        return []

    # Parse timestamps and sort the list
    timestamps_values = sorted(timestamps_values, key=lambda x: x[0])

    # Convert string timestamps to datetime objects
    timestamps_values = [(datetime.strptime(ts, "%Y-%m-%d %H:%M:%S"), value) for ts, value in timestamps_values]

    # Determine the start and end time
    start_time = timestamps_values[0][0]
    end_time = timestamps_values[-1][0]

    # Create a dictionary from the list for fast lookups
    values_dict = {ts: value for ts, value in timestamps_values}

    # Generate the complete list of timestamps with values
    current_time = start_time
    complete_timestamps_values = []

    while current_time <= end_time:
        if current_time in values_dict:
            complete_timestamps_values.append((current_time.strftime("%Y-%m-%d %H:%M:%S"), values_dict[current_time]))
        else:
            complete_timestamps_values.append((current_time.strftime("%Y-%m-%d %H:%M:%S"), 0))
        current_time += timedelta(seconds=1)

    return complete_timestamps_values




