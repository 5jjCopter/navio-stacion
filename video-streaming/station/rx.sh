#!/bin/bash
#
# Config grabbed from emlid.com navio2 docs
#
local_port="9000"

gst-launch-1.0 -v udpsrc port=$local_port \
caps='application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264' ! \
rtph264depay ! avdec_h264 ! \
videoconvert ! autovideosink sync=f
