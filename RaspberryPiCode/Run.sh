#!/bin/sh
echo "Starting to read your heart rate..." | piper --model en_US-lessac-medium --output_file intro.wav
aplay intro.wav
python3 PPGSerial.py
echo "Reading Complete" | piper --model en_US-lessac-medium --output_file outro.wav
aplay outro.wav
python3 calculations.py > out
cat out | piper --model en_US-lessac-medium --output_file reading.wav
aplay reading.wav
