import pandas as pd
from datetime import datetime
import time
from time import sleep
import subprocess
import signal
import os

def timeWindow(df, start_date, end_date):
    """
    Select rows within the specified date range from the DataFrame.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the timestamp column.
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        pandas.DataFrame: A new DataFrame containing only the rows within the specified date range.
    """
    # Convert the "Timestamp" column to datetime if it's not already in datetime format
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Use boolean indexing to select rows within the specified date range
    selected_rows = df[(df["Timestamp"] >= start_date) & (df["Timestamp"] <= end_date)].copy()

    # Reset index of the new DataFrame
    selected_rows.reset_index(drop=True, inplace=True)

    return selected_rows


def calcTimeDiff(t1,t2):

    format = "%Y-%m-%d %H:%M:%S"
    time1 = datetime.strptime(t1, format)
    time2 = datetime.strptime(t2, format)
    diff = abs(time2 - time1)
    return int(diff.total_seconds())


def initLog(tag):

    LOG_FILE = f".../PowerGuard/code/logs/log_activities/{tag}.log"

    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    # Return the path to the log file
    return LOG_FILE


def log_to_file(message,log_file):

    with open(log_file, 'a') as log_file:
        log_file.write(message)


def getMacAddress(device):

   devices = {

      'device1':  'mac1',
      'device2':  'mac2',
      ...
   }

   return devices[device]


def mapDataToDevice():

    maps = {

        "Sleep":                    <mapping>,
        "Other_Activity":           <mapping>,
        "Dress":                    <mapping>",
        "Personal_Hygiene":         <mapping>,
        "Phone":                    <mapping>,
        "Toilet":                   <mapping>,
        "Work_At_Table":            <mapping>,
        "Entertain_Guests" :        <mapping>,
        "Work_On_Computer":         <mapping>,
        "Cook_Breakfast" :          <mapping>,
        "Wash_Dishes" :             <mapping>,
        "Groom" :                   <mapping>,
        "Wash_Breakfast_Dishes":    <mapping>,
        "Bathe" :                   <mapping>,
        "Cook":                     <mapping>,
        "Relax":                    <mapping>,
        "Read":                     <mapping>,
        "Eat_Breakfast":            <mapping>,
        "Watch_TV":                 <mapping>,
        "Enter_Home":               <mapping>,
        "Leave_Home":               <mapping>,
        "Bed_Toilet_Transition":    <mapping>,
        "Cook_Lunch":               <mapping>,
        "Work":                     <mapping>,
        "Step_Out":                 <mapping>,
        "Wash_Lunch_Dishes":        <mapping>,
        "Cook_Dinner":              <mapping>,
        "Sleep_Out_Of_Bed":         <mapping>,
        "Wash_Dinner_Dishes":       <mapping>,
        "Eat_Dinner":               <mapping>,
        "Eat_Lunch":                <mapping>,
        "Eat":                      <mapping>,
        "Drink":                    <mapping>,
        "Evening_Meds":             <mapping>,
        "Morning_Meds":             <mapping>,

    }

    file_path = ".../month_data.txt"

    try:
        with open(file_path, 'r') as file:
            data_list = [line.strip().split('\t') for line in file]

        columns = ["Timestamp", "M007", "Room", "Furniture", "State", "Sensor", "Activity"]
        df = pd.DataFrame(data_list, columns=columns)
        df = df[["Timestamp", "Activity"]]

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Convert "Timestamp" to datetime format
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Group by minute and get the most common activity for each minute
    df = df.groupby([df["Timestamp"].dt.floor('T')])["Activity"].agg(lambda x: x.mode().iloc[0]).reset_index()

    # Add a new column for corresponding devices using the mapping
    df["Device"] = df["Activity"].map(maps)

    df_all = df.drop(columns=["Activity"])

    # The following here is responsible for selecting the time window of the experiment (date), and also give info to user.
    start_date  =   #example: "2012-11-01 00:00:00"
    end_date    =   #         "2012-11-02 00:00:00"
    df = timeWindow(df_all, start_date, end_date)
    unique_devices_day = df["Device"].unique()

    # used to extract the week's devices
    start_w  =  #example: "2012-10-27 00:00:00"
    end_w    =  #         "2012-11-03 00:00:00"
    dfweek = timeWindow(df_all, start_w, end_w)
    unique_devices = dfweek["Device"].unique()

    print("----------------------------------------------------------------------------------------------------------------------------------")
    print("Data Information:")
    print("----------------------------------------------------------------------------------------------------------------------------------")
    print("Number of data-points in selected time window: ",len(df))
    print("Time window length (hours):",calcTimeDiff(start_date,end_date)/(60*60))
    print("Devices utilized (day) :", ", ".join(unique_devices_day))
    print("Devices utilized (week) :", ", ".join(unique_devices))
    print("----------------------------------------------------------------------------------------------------------------------------------")



    static = df.iloc[0][1]
    count  = 0
    lst = []

    for row in range(1,len(df)):
        if static == df.iloc[row][1]:
            duration = calcTimeDiff(str(df.iloc[row-1][0]),str(df.iloc[row][0]))
            count += duration
            static = df.iloc[row][1]

        if static != df.iloc[row][1]:
            timediff = calcTimeDiff(str(df.iloc[row][0]),str(df.iloc[row-1][0]))
            if timediff > 60:
                lst.append(["nothing",timediff])
            if count == 0:
                # lst.append(["nothing",calcTimeDiff(str(df.iloc[row][0]),str(df.iloc[row-1][0]))])
                lst.append([df.iloc[row-1][1],calcTimeDiff(str(df.iloc[row][0]),str(df.iloc[row-1][0]))])
            if count >0:
                # lst.append(["nothing",calcTimeDiff(str(df.iloc[row][0]),str(df.iloc[row-1][0]))])
                lst.append([df.iloc[row-1][1],count+60])
            count = 0
            static = df.iloc[row][1]

    if count > 0 :
        lst.append([static,count])

    dfDuration = pd.DataFrame(lst, columns=["device","duration (seconds)"])
    # the following 2 lines are needed to remove "nothing" entries which are created in the begining
    # dfDuration = dfDuration.drop(dfDuration.index[0])
    # dfDuration = dfDuration.drop(dfDuration.index[0])

    print(dfDuration)

    # TEST CASE -------------------------------------------------------------------------------------
    # uncomment the following lines to test a specific device, edit the DEVICE and DURATION variables
    # new_row_data = {'device': <device>, 'duration (seconds)': <sec>}
    # dfDuration = pd.concat([pd.DataFrame(new_row_data, index=[0]), dfDuration], ignore_index=True)
    # -----------------------------------------------------------------------------------------------

    return dfDuration, unique_devices


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


def controller(df,devices_used):

    # The following are constants
    path = f".../PowerGuard/code/trigger_activities.sh"
    username = <username>
    password = <password>

    # The following start network and power capture
    print("Starting Network and Power capture...")
    print("Press CTRL + C twice to exit gracefully.")
    process = subprocess.Popen(["sudo","bash","measure_tapos.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file    = initLog(timestamp)
    log_to_file("     Start Time     |      End Time       |  State   |    Device     \n",log_file)
    log_to_file("--------------------|---------------------|----------|---------------\n",log_file)

    for dev_i in devices_used:

        exp_tag = getMacAddress(dev_i)
        subprocess.run(["sudo",".../opt/moniotr/bin/tag-experiment","start",exp_tag,dev_i]) #begin network capture of device. 

    try:

       for row in range(len(df)):

           duration = df.iloc[row][1]
           device   = df.iloc[row][0]
           print(f"running {device} for {duration} seconds")

           # The following is writting in the  log the start time of  activities.
           time_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

           if device == "nothing":
               # in case there is no activity, stay idle
               print("duration: ",duration)
               print("device: ",device)
               time.sleep(duration)

           # The elif statements are for special cases where the common triggering script is not sufficient
           elif device == <exception>:
              
              #add here any devices require further commands/ instructions.

           else:

               createInstruction(device,duration)
               config_fpath = device
               subprocess.run(["sudo", "bash", path, "--config_fpath", config_fpath])
               print("ending activity")

           # The following is writting in the log the end time of activities.
           time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           log_to_file(f"{time_start} | {time_end} |   actv   | {device}\n",log_file)

       print("Stoping network capture...")

       for dev_i in devices_used:

           exp_tag = getMacAddress(dev_i)
           subprocess.run(["sudo",".../opt/moniotr/bin/tag-experiment","stop",exp_tag,dev_i])

       print("Stoping power capture...")

       subprocess.run(["sudo","pkill","-f","getpow.py"]) # ensure power capture stops
       process.terminate()

    except (KeyboardInterrupt, Exception) as e:

       # This except statement is important in case something previously fails. Otherwise tagged experiments will remain open.
       print("-------------------------- ATTENTION !!! -------------------------------")
       print(f"Force quiting tagged experiments, {e}")

       for dev_i in devices_used:

           exp_tag = getMacAddress(dev_i)
           subprocess.run(["sudo",".../opt/moniotr/bin/tag-experiment","stop",exp_tag,dev_i])

       subprocess.run(["sudo","pkill","-f","python3","getpow.py"])
       process.terminate()

df, devices_used = mapDataToDevice()
controller(df,devices_used)
