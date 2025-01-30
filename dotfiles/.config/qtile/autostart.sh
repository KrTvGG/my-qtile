#!/bin/bash
# Stuff to be run at startup.
picom --experimental-backends &
walp &
qtile cmd-obj -o cmd -f restart
polybar &
volumeicon &
nm-applet &
