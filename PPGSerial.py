import serial
import time

# Configure the serial port
port = '/dev/ttyACM0'  
baudrate = 9600 
timeout = 1  

# Open the serial port
ser = serial.Serial(port, baudrate, timeout=timeout)

# Open a file to write the captured data
output_file = 'data.csv'

try:
    with open(output_file, 'w') as file:
        print(f"Capturing data from {port} and saving to {output_file}...")
        start_time = time.time()
        while True:
            # Read data from the serial port
            if time.time() - start_time > 30:
                print("60 seconds have passed. Stopping capture.")
                break  # Stop reading data after 60 seconds
            data = ser.readline().decode('utf-8').strip()
            
            if data:  # If data is received
                # Print to console (optional)
                file.write(data + '\n')  # Write to file
                
except KeyboardInterrupt:
    print("Capture interrupted by user.")

finally:
    ser.close()  # Close the serial port
    print("Serial port closed.")
