#!/bin/bash
remote_ip="192.168.100.147"
remote_port="9000"
width="960"
height="540"
bitrate="500000"

raspivid -n -w $width -h $height -b $bitrate -fps 15 -t 0 -o - | \
gst-launch-1.0 -v fdsrc ! h264parse ! \
rtph264pay config-interval=10 pt=96 ! \
udpsink host=$remote_ip port=$remote_port
