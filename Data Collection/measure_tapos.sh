#!/bin/bash

# List of devices to iterate over
devices=("device1" "device2" ...) # edit to place names of devices

# Number of times to run the Python program in parallel (same as number of devices)
NUM_RUNS=${#devices[@]}

# Loop to run the Python program with each device in parallel
for ((i = 0; i < NUM_RUNS; i++)); do
    nohup python3 getpow.py --d "${devices[i]}" &
done

wait

