#!/usr/bin/env python3
"""
PiAquaPulse - Water Quality Monitoring System

A Raspberry Pi Zero based system for monitoring water quality parameters:
- Temperature using DS18B20 waterproof sensor
- pH level using analog pH sensor via MCP3008
- Turbidity using SEN0189 sensor via MCP3008
- GPS location using NEO-6M module

Designed for field research and environmental monitoring applications.
"""

import os
import glob
import time
import datetime
import logging
import csv
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import serial
import pynmea2
import board
import busio
import digitalio
from threading import Timer
from pathlib import Path

# Configure logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{log_dir}/piaquapulse.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration constants
CONFIG = {
    # GPIO Pins
    'BUTTON_PIN': 17,
    'LED_PIN': 27,
    'ONE_WIRE_PIN': 4,  # DS18B20 data pin (BCM)
    # MCP3008 Configuration
    'CLK_PIN': 11,
    'MISO_PIN': 9,
    'MOSI_PIN': 10,
    'CS_PIN': 8,
    'PH_CHANNEL': 0,    # pH sensor on MCP3008 channel 0
    'TURBIDITY_CHANNEL': 1,  # Turbidity sensor on MCP3008 channel 1
    # Sensor calibration values
    'PH_4_VOLTAGE': 3.1,  # Voltage at pH 4 (calibration point)
    'PH_7_VOLTAGE': 2.6,  # Voltage at pH 7 (calibration point)
    # Serial port for GPS
    'GPS_PORT': '/dev/ttyS0',
    'GPS_BAUD': 9600,
    # Data storage
    'DATA_FILE': 'river_data.csv',
    # Automatic logging (seconds)
    'AUTO_LOG_INTERVAL': 300,  # Log every 5 minutes by default
}

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(CONFIG['BUTTON_PIN'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(CONFIG['LED_PIN'], GPIO.OUT)

# Initialize MCP3008 for analog sensors
mcp = Adafruit_MCP3008.MCP3008(
    clk=CONFIG['CLK_PIN'],
    cs=CONFIG['CS_PIN'],
    miso=CONFIG['MISO_PIN'],
    mosi=CONFIG['MOSI_PIN']
)

# Initialize 1-Wire interface for DS18B20
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
# Find the device file that corresponds to the temperature sensor
temp_sensor_folder = None

def initialize_temp_sensor():
    """Initialize and find the DS18B20 temperature sensor."""
    global temp_sensor_folder
    try:
        device_folders = glob.glob(base_dir + '28*')
        if device_folders:
            temp_sensor_folder = device_folders[0]
            logger.info(f"DS18B20 sensor found at: {temp_sensor_folder}")
            return True
        else:
            logger.error("DS18B20 sensor not found. Check connections.")
            return False
    except Exception as e:
        logger.error(f"Error initializing DS18B20 sensor: {e}")
        return False

def read_ds18b20():
    """
    Read temperature from DS18B20 sensor.
    
    Returns:
        float: Temperature in Celsius, or None if error
    """
    global temp_sensor_folder
    
    if not temp_sensor_folder:
        if not initialize_temp_sensor():
            return None
            
    try:
        device_file = temp_sensor_folder + '/w1_slave'
        with open(device_file, 'r') as f:
            lines = f.readlines()
            
        # Check if CRC is valid (YES at the end of first line)
        if lines[0].strip()[-3:] != 'YES':
            logger.warning("DS18B20 CRC check failed, retrying...")
            time.sleep(0.2)
            return read_ds18b20()
            
        # Extract temperature from second line
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            logger.debug(f"Raw temperature reading: {temp_c}°C")
            
            # Basic validation
            if -55.0 <= temp_c <= 125.0:  # DS18B20 operating range
                return round(temp_c, 2)
            else:
                logger.warning(f"DS18B20 reading out of range: {temp_c}°C")
                return None
    except Exception as e:
        logger.error(f"Error reading DS18B20 temperature: {e}")
        return None

def read_ph_sensor():
    """
    Read pH value from analog pH sensor via MCP3008.
    
    Returns:
        float: pH value (0-14 scale), or None if error
    """
    try:
        # Get average reading to reduce noise
        readings = []
        for _ in range(10):
            reading = mcp.read_adc(CONFIG['PH_CHANNEL'])
            readings.append(reading)
            time.sleep(0.1)
            
        # Remove highest and lowest readings and average the rest
        readings.remove(max(readings))
        readings.remove(min(readings))
        avg_reading = sum(readings) / len(readings)
        
        # Convert to voltage (0-1023 -> 0-3.3V)
        voltage = (avg_reading * 3.3) / 1023.0
        logger.debug(f"pH sensor voltage: {voltage}V")
        
        # Convert voltage to pH using calibration values
        # pH 4 and pH 7 calibration points create a linear relationship
        slope = (7.0 - 4.0) / (CONFIG['PH_7_VOLTAGE'] - CONFIG['PH_4_VOLTAGE'])
        ph_value = 7.0 + slope * (CONFIG['PH_7_VOLTAGE'] - voltage)
        
        # Basic validation
        if 0.0 <= ph_value <= 14.0:
            return round(ph_value, 2)
        else:
            logger.warning(f"pH reading out of range: {ph_value}")
            return None
    except Exception as e:
        logger.error(f"Error reading pH sensor: {e}")
        return None

def read_turbidity_sensor():
    """
    Read turbidity value from SEN0189 sensor via MCP3008.
    
    Returns:
        float: Turbidity in NTU (Nephelometric Turbidity Units), or None if error
    """
    try:
        # Get average reading to reduce noise
        readings = []
        for _ in range(10):
            reading = mcp.read_adc(CONFIG['TURBIDITY_CHANNEL'])
            readings.append(reading)
            time.sleep(0.1)
            
        # Remove highest and lowest readings and average the rest
        readings.remove(max(readings))
        readings.remove(min(readings))
        avg_reading = sum(readings) / len(readings)
        
        # Convert to voltage (0-1023 -> 0-3.3V)
        voltage = (avg_reading * 3.3) / 1023.0
        logger.debug(f"Turbidity sensor voltage: {voltage}V")
        
        # Convert voltage to NTU based on SEN0189 datasheet
        # Typically: voltage decreases as turbidity increases
        # This is an approximation and should be calibrated for your specific sensor
        if voltage > 2.5:
            ntu = 0  # Clear water
        else:
            # Polynomial approximation based on typical calibration curve
            # NTU = -1120.4*voltage*voltage + 5742.3*voltage - 4352.9
            # Simplified linear approximation:
            ntu = 3000 * (1 - voltage / 2.5)
            
        # Basic validation (SEN0189 range is typically 0-3000 NTU)
        if 0 <= ntu <= 3000:
            return round(ntu, 2)
        else:
            logger.warning(f"Turbidity reading out of range: {ntu} NTU")
            return None
    except Exception as e:
        logger.error(f"Error reading turbidity sensor: {e}")
        return None

def get_gps_data(timeout=10):
    """
    Get GPS coordinates from NEO-6M GPS module.
    
    Args:
        timeout: Time in seconds to wait for a GPS fix
        
    Returns:
        str: Comma-separated latitude,longitude, or None if error/timeout
    """
    try:
        # Open serial port
        with serial.Serial(CONFIG['GPS_PORT'], baudrate=CONFIG['GPS_BAUD'], timeout=1) as ser:
            start_time = time.time()
            
            # Try to get a valid GPS reading within timeout period
            while (time.time() - start_time) < timeout:
                line = ser.readline().decode('ascii', errors='replace').strip()
                
                # Look for GPRMC or GNRMC sentences which contain location data
                if line.startswith('$GPRMC') or line.startswith('$GNRMC'):
                    try:
                        msg = pynmea2.parse(line)
                        if msg.status == 'A':  # A=Active (valid), V=Void (invalid)
                            # Format coordinates as decimal degrees
                            lat = float(msg.latitude)
                            lon = float(msg.longitude)
                            logger.debug(f"GPS fix obtained: {lat}, {lon}")
                            return f"{lat:.6f},{lon:.6f}"
                    except Exception as e:
                        logger.debug(f"Error parsing NMEA sentence: {e}")
                
                # Brief pause to reduce CPU usage
                time.sleep(0.1)
                
            logger.warning(f"GPS timeout after {timeout} seconds, no valid fix")
            return None
    except Exception as e:
        logger.error(f"Error reading GPS module: {e}")
        return None

def ensure_data_file_exists():
    """Ensure that the data file exists with proper headers."""
    file_exists = os.path.isfile(CONFIG['DATA_FILE'])
    if not file_exists:
        try:
            logger.info(f"Creating new data file: {CONFIG['DATA_FILE']}")
            with open(CONFIG['DATA_FILE'], 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Timestamp', 
                    'Temperature (°C)', 
                    'pH', 
                    'Turbidity (NTU)', 
                    'GPS Location',
                    'Notes'
                ])
            return True
        except Exception as e:
            logger.error(f"Error creating data file: {e}")
            return False
    return True

def log_reading(manual=False):
    """
    Log sensor readings to the data file.
    
    Args:
        manual: Whether reading was triggered manually (True) or automatically (False)
    
    Returns:
        dict: Sensor readings, or None if error
    """
    try:
        # Turn on LED to indicate activity
        GPIO.output(CONFIG['LED_PIN'], GPIO.HIGH)
        
        # Get timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get sensor readings
        logger.info("Taking sensor readings...")
        temp = read_ds18b20()
        ph = read_ph_sensor()
        turbidity = read_turbidity_sensor()
        
        # Get GPS coordinates (with shorter timeout for manual readings)
        timeout = 5 if manual else 10
        coords = get_gps_data(timeout=timeout)
        
        # Create notes field
        notes = "Manual reading" if manual else "Auto reading"
        if temp is None: notes += ", Temp sensor error"
        if ph is None: notes += ", pH sensor error"
        if turbidity is None: notes += ", Turbidity sensor error"
        if coords is None: notes += ", No GPS fix"
        
        # Log sensor readings
        logger.info(f"Logging data: Temp={temp}°C, pH={ph}, Turbidity={turbidity}NTU, GPS={coords}")
        
        # Ensure data file exists
        if not ensure_data_file_exists():
            logger.error("Failed to ensure data file exists")
            GPIO.output(CONFIG['LED_PIN'], GPIO.LOW)
            return None
        
        # Write data to CSV file
        with open(CONFIG['DATA_FILE'], 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                temp if temp is not None else "ERROR",
                ph if ph is not None else "ERROR",
                turbidity if turbidity is not None else "ERROR",
                coords if coords is not None else "NO FIX",
                notes
            ])
        
        # Create reading dictionary to return
        reading = {
            'timestamp': timestamp,
            'temperature': temp,
            'ph': ph,
            'turbidity': turbidity,
            'gps': coords,
            'notes': notes
        }
        
        # Turn off LED
        GPIO.output(CONFIG['LED_PIN'], GPIO.LOW)
        
        # Blink LED to indicate success
        for _ in range(3):
            GPIO.output(CONFIG['LED_PIN'], GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(CONFIG['LED_PIN'], GPIO.LOW)
            time.sleep(0.1)
            
        return reading
        
    except Exception as e:
        logger.error(f"Error logging reading: {e}")
        # Ensure LED is off
        GPIO.output(CONFIG['LED_PIN'], GPIO.LOW)
        return None

def button_callback(channel):
    """Callback function for button press."""
    logger.info("Button press detected - manually logging readings")
    # Debounce button press
    time.sleep(0.2)
    if GPIO.input(channel) == GPIO.LOW:  # Confirm button is still pressed
        # Log readings
        reading = log_reading(manual=True)
        if reading:
            logger.info("Manual reading logged successfully")
        else:
            logger.error("Failed to log manual reading")

class AutoLogger:
    """Class to handle automatic logging at regular intervals."""
    def __init__(self, interval=CONFIG['AUTO_LOG_INTERVAL']):
        self.interval = interval
        self.timer = None
        self.running = False
        
    def start(self):
        """Start automatic logging."""
        self.running = True
        self.schedule_next()
        logger.info(f"Automatic logging started (every {self.interval} seconds)")
        
    def schedule_next(self):
        """Schedule the next automatic reading."""
        if self.running:
            self.timer = Timer(self.interval, self.log_and_reschedule)
            self.timer.daemon = True
            self.timer.start()
            
    def log_and_reschedule(self):
        """Log readings and schedule the next logging."""
        logger.info("Auto-logging triggered")
        reading = log_reading(manual=False)
        if reading:
            logger.info("Automatic reading logged successfully")
        else:
            logger.error("Failed to log automatic reading")
        self.schedule_next()
        
    def stop(self):
        """Stop automatic logging."""
        self.running = False
        if self.timer:
            self.timer.cancel()
        logger.info("Automatic logging stopped")

def cleanup():
    """Clean up resources before exit."""
    logger.info("Cleaning up resources...")
    # Stop automatic logging if running
    if auto_logger and auto_logger.running:
        auto_logger.stop()
    # Clean up GPIO
    GPIO.cleanup()
    logger.info("Cleanup complete")

if __name__ == "__main__":
    try:
        logger.info("Starting PiAquaPulse water quality monitoring system")
        
        # Blink LED to indicate startup
        for _ in range(5):
            GPIO.output(CONFIG['LED_PIN'], GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(CONFIG['LED_PIN'], GPIO.LOW)
            time.sleep(0.1)
        
        # Initialize temperature sensor
        if not initialize_temp_sensor():
            logger.warning("Temperature sensor not initialized, will retry later")
        
        # Set up button interrupt
        GPIO.add_event_detect(CONFIG['BUTTON_PIN'], GPIO.FALLING, 
                            callback=button_callback, bouncetime=300)
        
        # Create and ensure data file exists
        ensure_data_file_exists()
        
        # Start automatic logging
        auto_logger = AutoLogger()
        auto_logger.start()
        
        # Take initial reading
        logger.info("Taking initial reading...")
        log_reading(manual=False)
        
        # Main loop - keep program running
        logger.info("Entering main loop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt received, exiting...")
        
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
    finally:
        # Clean up resources
        cleanup()
        logger.info("PiAquaPulse system shutdown complete")
