import network
import time
import dht
import machine
import urequests  # HTTP requests library
import ujson
import math

# Ubidots credentials
UBIDOTS_TOKEN = "BBUS-7N0AEc9epgHgNM9NUO8O0BXF2jh4Ov"
UBIDOTS_URL = "https://industrial.api.ubidots.com/api/v1.6/devices/esp32test"

# WiFi credentials
WIFI_SSID = "Ruang Admin"
WIFI_PASS = "tanyaadmin"

# Initialize DHT11 sensor
dht_pin = machine.Pin(4)  # Change GPIO if needed
sensor = dht.DHT11(dht_pin)
ldr = machine.ADC(machine.Pin(32))  # Use GPIO34 (ADC1)
ldr.atten(machine.ADC.ATTN_11DB)  # Full range (0-3.3V)

R_FIXED = 10000  

# Constants for LDR (GL5528 example)
ldr_gamma = 0.7
ldr_rl10 = 50e3

# Connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)


    print("Connecting to WiFi...", end="")
    while not wlan.isconnected():
        time.sleep(1)
        print(".", end="")
    print("\nWiFi Connected:", wlan.ifconfig())
    print(network.WLAN(network.STA_IF).ifconfig())

# Send data using HTTP
def send_data(temp, hum, ldr):
    headers = {
        "X-Auth-Token": UBIDOTS_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "temperature": {"value": temp},
        "humidity": {"value": hum},
        "ldr": {"value": ldr}
    }

    print("Sending data to Ubidots...", payload)
    # response = urequests.post(UBIDOTS_URL, json=payload, headers=headers)
    # print("Response:", response.text)
    # if response.status_code == 200 or response.status_code == 201:
    #     print("✅ Data sent successfully:", response.json())
    # else:
    #     print(f"⚠️ Error: {response.status_code}")
    #     print("Response:", response.json())  # Output full error JSON
    flask_res = urequests.post("http://192.168.77.164:5000/sensor_data", json=payload, headers=headers)
    if (flask_res.status_code != 200):
        print("Error sending data: ", flask_res.json())
    else:
        print("sending data succeses")
    # response.close()
    flask_res.close()


# Main loop
connect_wifi()
while True:
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()
    ldr_value = ldr.read()
    volt = ldr_value / (4095 - ldr_value)

    res = 10e3 * volt
    lux = 0 if res == 0 else 10 * math.pow(ldr_rl10/res, 1/ldr_gamma)
    
    print(f"Temp: {temperature}°C, Humidity: {humidity}%")
    send_data(temperature, humidity, lux)
        

    time.sleep(10)  # Send data every 10 seconds


