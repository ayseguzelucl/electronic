
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





def separation(device,hm):

    """
      Description:

          The following function is responsible for the labeling of the data, based
          on the log file contents. It seperates the data with a granularity of 1 minutes.

      Input Args:
          device, dictionary (either power, or nwtwork)
    """
    device_df = log_hm[log_hm['Device'] == device]
    lst_state = device_df['State'].unique()
    lst_state = lst_state[:-1] # -1 to remove resting

    xlst  = []
    ylst  = []
    stLst = []

    for state in lst_state:
        state_df = device_df[device_df['State'] == state]
        label , status   = stateMap(state)
        for i in range(len(state_df)):
            start_time = state_df["Start Time"].iloc[i]
            end_time   = state_df["End Time"].iloc[i]
            Lst = []
            for timestamp, net in hm[device]:
                if pd.to_datetime(start_time) <= pd.to_datetime(timestamp) <= pd.to_datetime(end_time):
                    Lst.append(net)
            xlst.append(Lst)
            ylst.append(label)
            stLst.append(status)

    return xlst, ylst, stLst
