from machine import Pin
from dht import DHT22
from time import sleep

sensor = DHT22(Pin(2)) # GPIO 2
led = Pin("LED", Pin.OUT) 
led.on() 

# Conections guide:
# Power: Pin 36 (3V3 (OUT))
# Data: Pin 4 (GP2)
# Ground: Pin 8 (GND)

def read_sensor():
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        return temperature, humidity
    except Exception as e:
        print('Failed to read sensor:', str(e))
        return None, None

print('DHT22 Temperature and Humidity Monitor')
print('Press Ctrl+C to stop')

while True:
    try:
        temp, hum = read_sensor() 
        if temp is not None and hum is not None:
            print(f'Temperature: {temp:.1f} C')
            print(f'Humidity: {hum:.1f}%')
            print('-------------------')
        sleep(0.2)  
    except KeyboardInterrupt:
        led.off()  
        print('Monitoring stopped')
        break
    except Exception as e:
        print('Error:', str(e))
        sleep(3) 