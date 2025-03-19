# **Circuit Documentation**

## **Summary**

This circuit is designed for a water quality monitoring system named PiAquaPulse. It utilizes a Raspberry Pi Zero as the central processing unit to monitor various parameters such as temperature, pH level, turbidity, and GPS location. The system is intended for field research and environmental monitoring applications.

## **Component List**

### **Turbidity Sensor**

* Pins: OUT, VCC, GND  
* Description: Measures the turbidity of water.

### **MCP3008 8-channel 10-bit ADC**

* Pins: \[See Component Documentation \- [https://docs.cirkitdesigner.com/component/53b70bdd-7e78-f112-b52d-8a154a5c3517](https://docs.cirkitdesigner.com/component/53b70bdd-7e78-f112-b52d-8a154a5c3517)\]  
* Description: Analog-to-digital converter used to read analog sensor data.

### **NEO 6M**

* Pins: VCC, RX, TX, GND  
* Description: GPS module for location tracking.

### **MKE-S15 DS18B20 Waterproof Temperature Sensor**

* Pins: SIG, 5V, GND  
* Description: Measures water temperature.

### **Analog pH Sensor Kit**

* Pins: Analog pin, \+9V pin, GND  
* Description: Measures the pH level of water.

### **LED: Two Pin (blue)**

* Pins: Cathode, Anode  
* Description: Indicates system status.

### **Resistor (4.7k Ohms)**

* Pins: Pin1, Pin2  
* Description: Pull-up resistor for temperature sensor.

### **Raspberry Pi Zero**

* Pins: Multiple GPIO and power pins  
* Description: Microcontroller for processing and control.

### **Resistor (10k Ohms)**

* Pins: Pin1, Pin2  
* Description: Pull-up resistor for button debounce.

### **Resistor (220 Ohms)**

* Pins: Pin1, Pin2  
* Description: Current limiting resistor for LED.

### **Push Button Round**

* Pins: Leg0, Leg1  
* Description: User input for manual data logging.

## 

## **Wiring Details**

### **Turbidity Sensor**

* OUT: Connected to MCP3008 ADC Channel 0  
* VCC: Connected to Raspberry Pi Zero 5V  
* GND: Common ground with other components

### **MCP3008 8-channel 10-bit ADC**

* \[To be named\]: Connected to various sensors and Raspberry Pi Zero GPIOs for data communication  
* Connect VDD to 3.3V  
* Connect VREF to 3.3V  
* Connect AGND to ground  
* Connect DGND to ground  
* Connect CLK to GPIO11 (pin 23, SPI0 SCLK)  
* Connect DOUT to GPIO9 (pin 21, SPI0 MISO)  
* Connect DIN to GPIO10 (pin 19, SPI0 MOSI)  
* Connect CS to GPIO8 (pin 24, SPI0 CE0)  
* Connect Channel 0 to pH Sensor  
* Connect Channel 1 to Turbidity Sensor

### **NEO 6M**

* VCC: Connected to Raspberry Pi Zero 5V  
* RX: Connected to Raspberry Pi Zero GPIO14  
* TX: Connected to Raspberry Pi Zero GPIO15  
* GND: Common ground with other components

### **MKE-S15 DS18B20 Waterproof Temperature Sensor**

* SIG: Connected to Raspberry Pi Zero GPIO4 through a 4.7k Ohms resistor  
* 5V: Connected to Raspberry Pi Zero 3.3V  
* GND: Common ground with other components

### **Analog pH Sensor Kit**

* Analog pin: Connected to MCP3008 ADC Channel 1  
* \+9V pin: Connected to Raspberry Pi Zero 5V  
* GND: Common ground with other components

### **LED: Two Pin (blue)**

* Cathode: Connected to common ground with other components  
* Anode: Connected to Raspberry Pi Zero GPIO27 through a 220 Ohms resistor

### **Resistor (4.7k Ohms)**

* Pin1: Connected to Raspberry Pi Zero 3.3V  
* Pin2: Connected to MKE-S15 DS18B20 Waterproof Temperature Sensor SIG

### **Raspberry Pi Zero**

* Utilizes multiple GPIO pins for interfacing with sensors and controls

### **Resistor (10k Ohms)**

* Pin1: Connected to Raspberry Pi Zero GPIO17  
* Pin2: Connected to Push Button Round Leg1

### **Resistor (220 Ohms)**

* Pin1: Connected to Raspberry Pi Zero GPIO27  
* Pin2: Connected to LED Anode

### **Push Button Round**

* Leg0: Connected to common ground with other components  
* Leg1: Connected to Raspberry Pi Zero GPIO17 through a 10k Ohms resistor

## **Documented Code**

The code provided is a Python script designed to run on the Raspberry Pi Zero. It includes functionality for initializing and reading from the connected sensors, logging data to a CSV file, and handling user input through a push button. The code also includes a GPS data retrieval function that reads from the NEO 6M GPS module.  
`#!/usr/bin/env python3`  
`"""`  
`PiAquaPulse - Water Quality Monitoring System`

`A Raspberry Pi Zero based system for monitoring water quality parameters:`  
`- Temperature using DS18B20 waterproof sensor`  
`- pH level using analog pH sensor via MCP3008`  
`- Turbidity using SEN0189 sensor via MCP3008`  
`- GPS location using NEO-6M module`

`Designed for field research and environmental monitoring applications.`  
`"""`

`# [Code continues...]`

The script is well-documented with comments explaining each section and function. It uses several libraries for interfacing with the hardware, such as RPi.GPIO for GPIO pin control, Adafruit\_MCP3008 for the ADC, and pynmea2 for parsing GPS data. The code is structured to run continuously, taking sensor readings at regular intervals and logging them to a file, with the ability to take manual readings via a push button.  
(Note: The full code is not displayed here due to length constraints, but it includes functions for reading each sensor, logging data, and handling button presses.)