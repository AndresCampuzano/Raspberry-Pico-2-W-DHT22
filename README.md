# Raspberry Pi Pico DHT22 Monitor

This project uses a Raspberry Pi Pico to monitor temperature and humidity with a DHT22 sensor. The data is read, adjusted for calibration, and optionally sent to a remote weather API. The device also connects to a WiFi network for data transmission.

## Features
- Reads temperature and humidity from the DHT22 sensor.
- Posts data to a weather API.
- Includes WiFi connectivity with automatic reconnection.
- LED indicators for device status.

## Example Output
```
-------------------
Temperature: 24.8 C
Humidity: 73.0%
-------------------
```
