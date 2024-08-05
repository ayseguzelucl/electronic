# PowerGuard

This repository contains the code of PowerGuard, a research aiming for the detection of network attacks through power consumption. The code in this repository can be used to automatically trigger activities, record the power traces through Tapo TP-Link Kasa P110 power plugs, and also track the network traffic of the devices using Mon(IoT)r. The code generates DoS SYN-flood attacks using the hping3 library.

## Data

The Power consumption and Network Traffic data collected in our experiments are publicly available at the link provided in the data file of this repository.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)

## Prerequisites

### Software Requirements
- Linux Ubuntu LTS24
- Python 3.9 or Newer
- Mon(IoT)r

### Hardware Requirements
- Local WiFi access point
- Testbed devices
- Tapo TPlink Kasa P110
- Google Pixel 2(or other Android phone specified in `/Data Collection/phone_ids`)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2. Install the necessary dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

The code is organized into 2 main directories:

**1. Data Collection**

This directory contains all of the code used for the collection of our data. The explanation of each file is as follows:

   *a)  getpow.py*

This Python script is used to record the power consumption of a selected device using the corresponding Tapo Power plug, that the device is attached to. The script automatically creates a dictionary (log_power) and a log file for the device, in which it appends the reading with its corresponding timestamp. The input argument of this script is the targeted device. Within the script, there is a dictionary (devtapo) that must be edited with the testbed configuration of the device-tapo pairs. The tapo id's must be clearly stated in the devices.txt files in the Mon(IoT)r directory  `(./opt/moniotr/etc/devices.txt) `

   *b) measure_tapos.sh*

This bash script activates all power recordings simultaneously for the testbed. The for which are to be selected can be edited within the list `devices=("device1" "device2" ...)`, where device1 is the device connected to the tapo power plug (i.e television).

   *c) pcapmaker.sh*

The following bash script is used to convert the pcap files into a more readable text file format containing timestamp-traffic volume pairs for each instance recorded by Mon(IoT)r. The source pcap file and destination txt file must be edited within the file. 

   *d) restpow.py*

During the sequence experiments, the tapo devices are switched off and on after each state. To achieve that, this script is used. Its operational requirements are the same with the getpow.py script. 

   *e) trigger_activities.sh*

This bash script governs the smartphone coordinate taping, allowing for the automation of the activity triggering. The Script initially checks if the phone/s specified in the `.../phone_ids` directory is connected to the server, then proceeds with the triggering of the activity for 1 device at a time. The instructions and device application details are read from an external file ((`.../logs/log_instructions/`)which is created automatically from the scripts in *f,g*. Note that the current configuration of the script allows for an initial tap, following a delay following a second tap. 
   
   *f) sequence_controller.py*

This Python script is used to control the 4-state sequence (idle, active, idle w attack, active w attack) experiments. The length of duration of each state, number of repetitions, and devices can be adjusted within the script. The script automatically creates a log file for each device it operates with, recording the start and end timestamps, along with the state and device id (`.../logs/log_activities/`). A finite state machine governs the order and nature of each state. During the flood attacks, the attack states, the command used is hping3, and the parameters of the attack can be adjusted as required. The instructions of the active states are selected in the `createInstructions` function.

   *g) week_controller.py*

This Python script is used to control the 1-week experiment. The script initially maps the selected period from the real-user study dataset to the testbed configuration. **Our work used the CASAS hh113 dataset, and the `month_data.txt` contains a 1-month snippet of the data that we used**. The mappings can be edited through the `mapDataToDevice` function as required. The testbed devices must also be stated in the `getMacAddress` function, along with their corresponding Mac addresses. Similarly to *f*, the device instructions for each active state can be set via the `createInstructions` function, and the activities are recorded in the log file found in `.../logs/log_activities/`.

   *h) week_attacker.py*

This Python script is to be used simultaneously with *g*, to inject a pre-determined number of DoS attacks in random devices for random durations along a pre-determined time window. The attacks are recorded in the (`.../logs/log_attacks/`)


**2. Data Processing**

This directory contains all the code that was used for the data processing, evaluation, and analysis. 

*a) dataloader.py*

The following is a simple Python script power, network, and log data that are to be used in subsequent modules. It also includes all libraries to be used for processing.

*b) formatting.py*

In this script, the data are initially ensured to have a reading for each second, as the network traffic that is captured using Mon(IoT)r will not give a reading in cases where the total network traffic is 0 Bytes. Subsequently, the script separates the data based on the labels and their granularity. For our work, we have chosen 1 minute to be the time window of separation. The state map function contains the labels for each state as determined by the user. For our case, the cases where there is no attack are 0 and with attack 1. 

 *c) preprocessing.py*

The preprocessing of the data can be completed based on a conditional imposed by the user. There are several features available, along with the raw signal.  

 *d) processing.py*

 The processing script consists of two architecture options, a Deep Neural Networks (DNN) with 8 hidden layers and dropout and a One-Class Support Vector Machine (SVM). The user can select which one to use using the input argument `model`. This script also contains the metrics to be used, and the repetition loop to rerun the entire process for a pre-determined amount of iterations.

 *e) plotting.py*

This script contains the plotting functions that are used to visualize the network traffic and the power consumption (or both) along any time window for the data. The function also considers the states at each timestamp and highlights any specific states specified by the user (i.e attack, idle).
 
