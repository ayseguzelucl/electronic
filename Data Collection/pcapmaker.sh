#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <pcap_file_path>"
    exit 1
fi

pcap_path="$1"

tshark -r "$pcap_path" -T fields -e frame.time_epoch | awk '{
  sec = int($1);
  count[sec]++;
} END {
  for (t in count) {
    print strftime("%Y-%m-%d %H:%M:%S", t), count[t];
  }
}' | sort > <device.txt>
