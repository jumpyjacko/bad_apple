#!/bin/bash

mpv --quiet ./assets/bad_apple.mp4 &

# Wait until the window appears
while ! xdotool search --name "mpv" > /dev/null 2>&1; do sleep 0.05; done

# Then run your command
./target/release/main
