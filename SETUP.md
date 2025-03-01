# PiAquaPulse Setup Guide

This guide provides step-by-step instructions for setting up the PiAquaPulse water quality monitoring system on a Raspberry Pi Zero.

## Hardware Requirements

- Raspberry Pi Zero W/2W
- DS18B20 waterproof temperature sensor
- Gravity analog pH sensor
- SEN0189 turbidity sensor
- MCP3008 analog-to-digital converter
- NEO-6M GPS module
- Push button
- LED indicator (preferably RGB)
- Micro SD card (8GB+)
- Power supply for Raspberry Pi Zero
- Breadboard and jumper wires
- Waterproof enclosure (optional but recommended)

## Hardware Connections

### DS18B20 Temperature Sensor
- Connect VCC to 3.3V
- Connect GND to ground
- Connect DATA to GPIO4 (pin 7)
- Add a 4.7K ohm resistor between VCC and DATA

### MCP3008 ADC (for pH and Turbidity sensors)
- Connect VDD to 3.3V
- Connect VREF to 3.3V
- Connect AGND to ground
- Connect DGND to ground
- Connect CLK to GPIO11 (pin 23, SPI0 SCLK)
- Connect DOUT to GPIO9 (pin 21, SPI0 MISO)
- Connect DIN to GPIO10 (pin 19, SPI0 MOSI)
- Connect CS to GPIO8 (pin 24, SPI0 CE0)

### pH Sensor
- Connect VCC to 5V
- Connect GND to ground
- Connect Analog Output to Channel 0 on MCP3008

### Turbidity Sensor
- Connect VCC to 5V
- Connect GND to ground
- Connect Analog Output to Channel 1 on MCP3008

### GPS Module (NEO-6M)
- Connect VCC to 5V
- Connect GND to ground
- Connect TX to GPIO15 (pin 10, UART RX)
- Connect RX to GPIO14 (pin 8, UART TX)

### Push Button
- Connect one terminal to GPIO17 (pin 11)
- Connect the other terminal to ground
- Add a 10K ohm pull-up resistor between 3.3V and the GPIO pin

### LED Indicator
- Connect the cathode (negative, longer leg) to ground
- Connect the anode (positive, shorter leg) to GPIO27 (pin 13) through a 220-330 ohm resistor

## Software Installation

### 1. Set up Raspberry Pi OS

1. Download and install the Raspberry Pi Imager from [raspberrypi.org](https://www.raspberrypi.org/software/)
2. Insert your microSD card into your computer
3. Launch the Raspberry Pi Imager
4. Select "Raspberry Pi OS Lite (32-bit)" as the operating system
5. Select your microSD card as the storage
6. Click on the gear icon to access advanced options:
- Enable SSH
- Configure Wi-Fi with your network details
- Set a hostname (e.g., piaquapulse)
- Set username and password
7. Click "Write" to flash the OS to the card
8. Insert the microSD card into your Raspberry Pi Zero and power it on

### 2. Update the system

```bash
sudo apt update
sudo apt upgrade -y
```

### 3. Enable required interfaces

```bash
sudo raspi-config
```

Navigate to "Interface Options" and enable:
- SPI
- I2C
- 1-Wire
- Serial Port (disable serial console, enable serial hardware)

Reboot after making these changes:
```bash
sudo reboot
```

### 4. Install required packages

```bash
sudo apt install -y python3-pip python3-dev git i2c-tools
sudo pip3 install --upgrade pip
```

### 5. Clone the repository

```bash
git clone https://github.com/your-username/PiAquaPulse.git
cd PiAquaPulse
```

### 6. Install Python dependencies

```bash
sudo pip3 install -r requirements.txt
```

## Configuring the System

### 1. Enable 1-Wire interface for temperature sensor

Edit the config file:
```bash
sudo nano /boot/config.txt
```

Add the following line at the end:
```
dtoverlay=w1-gpio,gpiopin=4
```

Save and exit (Ctrl+X, Y, Enter)

### 2. Enable UART for GPS module

Edit the config file if you haven't already:
```bash
sudo nano /boot/config.txt
```

Add these lines if they don't exist:
```
enable_uart=1
dtoverlay=disable-bt
```

Save and exit, then reboot:
```bash
sudo reboot
```

## Running the PiAquaPulse System

### 1. Manual execution

```bash
cd PiAquaPulse
python3 PAPScript.py
```

### 2. Set up automatic startup on boot

Create a service file:
```bash
sudo nano /etc/systemd/system/piaquapulse.service
```

Add the following content:
```
[Unit]
Description=PiAquaPulse Water Quality Monitoring
After=multi-user.target

[Service]
User=pi
WorkingDirectory=/home/pi/PiAquaPulse
ExecStart=/usr/bin/python3 /home/pi/PiAquaPulse/PAPScript.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable piaquapulse.service
sudo systemctl start piaquapulse.service
```

### 3. Check service status

```bash
sudo systemctl status piaquapulse.service
```

## Usage Instructions

### Manual Data Logging
- Press the push button to manually log a data point
- The LED will briefly flash to confirm the logging

### Automatic Logging
- The system automatically logs data at the interval configured in PAPScript.py (default: 5 minutes)
- The LED will briefly flash during each automatic logging event

### Accessing Logged Data
- Data is stored in CSV format at `/home/pi/PiAquaPulse/data/water_quality_data.csv`
- Transfer files using SCP, SFTP, or by setting up a simple web server

### LED Status Indicators
- Solid on: System initializing
- Quick flash: Data point logged
- Slow regular flashing: Error condition
- Off: Normal operation (to conserve power)

### Troubleshooting
- Check the log file at `/home/pi/PiAquaPulse/logs/system.log` for error messages
- Ensure all sensors are properly connected
- Verify the system has proper permissions to access the GPIO pins
- For GPS issues, ensure the module has clear view of the sky

## Maintenance

- Calibrate the pH sensor regularly using standard buffer solutions
- Clean the turbidity sensor probe as needed
- Keep the waterproof enclosure sealed properly
- Check the data logs periodically to ensure proper operation
- Consider setting up a cron job to trim log files and back up data

## Additional Resources

- [Raspberry Pi GPIO Documentation](https://www.raspberrypi.org/documentation/hardware/raspberrypi/gpio/README.md)
- [DS18B20 Datasheet](https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf)
- [MCP3008 Datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/21295d.pdf)
- [NEO-6M GPS Module Documentation](https://www.u-blox.com/sites/default/files/products/documents/NEO-6_DataSheet_(GPS.G6-HW-09005).pdf)

