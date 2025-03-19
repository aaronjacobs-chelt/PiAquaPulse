/*
 * Water Quality Monitoring System
 *
 * This Arduino sketch reads data from various sensors:
 * - DS18B20 for temperature
 * - Analog pH sensor via MCP3008
 * - Turbidity sensor via MCP3008
 * - NEO-6M GPS module
 *
 * The system logs data to a CSV file on an SD card when a button is pressed.
 * An LED flashes to indicate activity.
 */

#include <SPI.h>
#include <SD.h>
#include <Adafruit_MCP3008.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <SoftwareSerial.h>

// Pin configuration
const int buttonPin = 17;
const int ledPin = 27;
const int oneWireBus = 4;
const int chipSelect = 10;

// MCP3008 configuration
Adafruit_MCP3008 mcp;
const int phChannel = 0;
const int turbidityChannel = 1;

// DS18B20 configuration
OneWire oneWire(oneWireBus);
DallasTemperature sensors(&oneWire);

// GPS configuration
SoftwareSerial gpsSerial(14, 15); // RX, TX

// CSV file
File dataFile;

void setup() {
  Serial.begin(9600);
  gpsSerial.begin(9600);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
  if (!SD.begin(chipSelect)) {
    Serial.println("SD card initialization failed!");
    return;
  }
  mcp.begin();
  sensors.begin();
  Serial.println("System initialized.");
}

void loop() {
  if (digitalRead(buttonPin) == LOW) {
    digitalWrite(ledPin, HIGH);
    delay(100);
    digitalWrite(ledPin, LOW);
    logData();
    delay(1000); // Debounce delay
  }
}

void logData() {
  sensors.requestTemperatures();
  float temperatureC = sensors.getTempCByIndex(0);
  int phReading = mcp.readADC(phChannel);
  int turbidityReading = mcp.readADC(turbidityChannel);
  float phVoltage = (phReading * 3.3) / 1023.0;
  float turbidityVoltage = (turbidityReading * 3.3) / 1023.0;
  float phValue = calculatePH(phVoltage);
  float turbidityNTU = calculateTurbidity(turbidityVoltage);
  String gpsData = getGPSData();
  dataFile = SD.open("data.csv", FILE_WRITE);
  if (dataFile) {
    dataFile.print(millis());
    dataFile.print(",");
    dataFile.print(temperatureC);
    dataFile.print(",");
    dataFile.print(phValue);
    dataFile.print(",");
    dataFile.print(turbidityNTU);
    dataFile.print(",");
    dataFile.println(gpsData);
    dataFile.close();
    Serial.println("Data logged.");
  } else {
    Serial.println("Error opening data file.");
  }
}

float calculatePH(float voltage) {
  float slope = (7.0 - 4.0) / (2.6 - 3.1);
  return 7.0 + slope * (2.6 - voltage);
}

float calculateTurbidity(float voltage) {
  if (voltage > 2.5) return 0;
  return 3000 * (1 - voltage / 2.5);
}

String getGPSData() {
  String nmeaData = "";
  while (gpsSerial.available()) {
    char c = gpsSerial.read();
    nmeaData += c;
    if (c == '\n') break;
  }
  return parseGPS(nmeaData);
}

String parseGPS(String nmea) {
  if (nmea.startsWith("$GPRMC")) {
    int latIndex = nmea.indexOf(",", 20);
    int lonIndex = nmea.indexOf(",", latIndex + 1);
    String latitude = nmea.substring(latIndex + 1, lonIndex);
    String longitude = nmea.substring(lonIndex + 1, nmea.indexOf(",", lonIndex + 1));
    return latitude + "," + longitude;
  }
  return "NO FIX";
}
