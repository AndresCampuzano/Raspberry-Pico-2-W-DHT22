from machine import Pin
from dht import DHT22
from time import sleep
import urequests
import network  # Import network module

sensor = DHT22(Pin(2))
raspberryLed = Pin("LED", Pin.OUT) 
raspberryLed.on()
customLed = Pin(15, Pin.OUT)
customLed.on()

# Connections guide:
# Power: Pin 36 (3V3 (OUT))
# Data: Pin 4 (GP2)
# Ground: Pin 8 (GND)

# Connect to WiFi
ssid = ''
password = ''

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    timeout = 10  # Timeout after 10 seconds
    while not wlan.isconnected() and timeout > 0:
        print('Connecting to network...')
        sleep(1)
        timeout -= 1
    if wlan.isconnected():
        print('Connected to', ssid)
        print('Network config:', wlan.ifconfig())
    else:
        print('Failed to connect to network')
        wlan.active(False)

def check_wifi_connection():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('WiFi connection lost. Attempting to reconnect...')
        wlan.active(False)
        sleep(1)
        wlan.active(True)
        connect_wifi()
        return wlan.isconnected()
    return True

connect_wifi()  # Connect to WiFi

def read_sensor():
    try:
        sensor.measure()
        temperature = sensor.temperature() - 2  # Adjust DTH22 sensor reading due to calibration
        humidity = sensor.humidity()
        return temperature, humidity
    except Exception as e:
        print('Failed to read sensor:', str(e))
        return None, None

def post_weather_data(temp, hum):
    url = ''
    data = {
        'temperature': temp,
        'humidity': hum,
        'city_id': '22fd2af8-2ea4-40f5-96f5-ffc8ab197d9f'
    }
    try:
        response = urequests.post(url, json=data)
        if response.status_code == 200:
            print('Data posted successfully')
        else:
            print('Failed to post data:', response.status_code)
        response.close()
    except OSError as e:
        print('Network error posting data:', str(e))
    except Exception as e:
        print('Error posting data:', str(e))

print('DHT22 Temperature and Humidity Monitor')
print('Press Ctrl+C to stop')

while True:
    try:
        temp, hum = read_sensor() 
        if temp is not None and hum is not None:
            print(f'Temperature: {temp:.1f} C')
            print(f'Humidity: {hum:.1f}%')
            print('-------------------')
            if check_wifi_connection():  # Check WiFi connection before posting
                post_weather_data(temp, hum)
            else:
                print('Skipping data post due to WiFi connection issues')
        sleep(60)  
    except KeyboardInterrupt:
        raspberryLed.off()  
        print('Monitoring stopped')
        break
    except Exception as e:
        print('Error:', str(e))
        sleep(3) 
