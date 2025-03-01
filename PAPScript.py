[200~# Basic Circuit Plan for PiAquaPulse using Raspberry Pi Zero

# Components:
# - Raspberry Pi Zero W/2W
# - DS18B20 Waterproof Temperature Sensor (1-Wire)
# - Gravity Analog pH Sensor
# - SEN0189 Turbidity Sensor
# - GPS Module (NEO-6M)
# - Push Button (for manual logging)
# - LED Indicator (for status feedback)
# - Power Supply (USB Power Bank)
# - Waterproof Connectors (GX12-4P for sensors, PG7 cable glands for wiring pass-through)

# GPIO Pin Assignments (subject to adjustment):
# - DS18B20: GPIO4 (1-Wire Data), 3.3V Power, GND
# - pH Sensor: ADC via MCP3008 (SPI Interface)
# - Turbidity Sensor: ADC via MCP3008 (SPI Interface)
# - GPS Module: UART (TX/RX to GPIO14/15)
# - Push Button: GPIO17
# - LED Indicator: GPIO27

# Wiring for GX12-4P Waterproof Connectors:
# - Pin 1: VCC (3.3V/5V depending on sensor)
# - Pin 2: GND
# - Pin 3: Signal/Data Line
# - Pin 4: Optional (e.g., second signal line or additional power)

import RPi.GPIO as GPIO
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Push Button
GPIO.setup(27, GPIO.OUT)  # LED Indicator

# Function to log data manually
def log_data():
    GPIO.output(27, GPIO.HIGH)  # Turn LED on
    print("Logging data...")
    # Read sensor data (Placeholder)
    temperature = read_ds18b20()
    pH_value = read_ph_sensor()
    turbidity = read_turbidity_sensor()
    gps_location = get_gps_data()
    
    # Save to file
    with open("river_data.csv", "a") as file:
        file.write(f"{time.time()},{temperature},{pH_value},{turbidity},{gps_location}\n")
    
    GPIO.output(27, GPIO.LOW)  # Turn LED off
    print("Data logged.")

# Event detection for button press
GPIO.add_event_detect(17, GPIO.FALLING, callback=lambda x: log_data(), bouncetime=300)

# Placeholder sensor functions
def read_ds18b20():
    return 20.5  # Example temperature reading

def read_ph_sensor():
    return 7.2  # Example pH reading

def read_turbidity_sensor():
    return 5.0  # Example NTU reading

def get_gps_data():
    return "51.509865,-0.118092"  # Example GPS coordinates

# Main loop (keeps script running)
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()

