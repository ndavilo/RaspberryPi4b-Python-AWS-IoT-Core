import json
import time
from gpiozero import LED
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import threading
import os
from dotenv import load_dotenv

# AWS IoT Core Configuration
endpoint = os.getenv("ENDPOINT")
port = int(os.getenv("PORT"))  # Convert to integer since port is numeric
topic = os.getenv("TOPIC")

# Certificate and Keys
cert_path = os.getenv("CERT_PATH")
key_path = os.getenv("KEY_PATH")
root_ca_path = os.getenv("ROOT_CA_PATH")

# MQTT Client Setup
mqtt_client = AWSIoTMQTTClient("raspberry_pi")
mqtt_client.configureEndpoint(endpoint, port)
mqtt_client.configureCredentials(root_ca_path, key_path, cert_path)

# Connection configuration
mqtt_client.configureAutoReconnectBackoffTime(1, 32, 20)
mqtt_client.configureOfflinePublishQueueing(-1)
mqtt_client.configureDrainingFrequency(2)
mqtt_client.configureConnectDisconnectTimeout(10)
mqtt_client.configureMQTTOperationTimeout(5)

# Connect to AWS IoT Core
mqtt_client.connect()

# Dictionary to store LED objects
led_dict = {}

# Function to control the switch based on received message
def control_switch(payload):
    try:
        data = json.loads(payload)
        switch = data['switch']
        state = data['state']
        
        # Initialize LED object if not already created
        if switch not in led_dict:
            led_dict[switch] = LED(switch)
        
        # Control the switch based on the state
        led = led_dict[switch]
        if state == "on":
            led.off() # the switch is reversed
        elif state == "off":
            led.on()
        else:
            print("Invalid state received:", state)

        # Add a delay after switching
        time.sleep(1)  # Adjust the delay time as needed
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    except KeyError as e:
        print("Missing key in payload:", e)

# Function to handle incoming messages
def message_callback(client, userdata, message):
    print("Message received from AWS IoT Core:", message.payload.decode())
    # Spawn a new thread to handle the switch control
    threading.Thread(target=control_switch, args=(message.payload.decode(),)).start()

# Subscribe to the topic to receive messages
mqtt_client.subscribe(topic, 1, message_callback)

try:
    while True:
        time.sleep(1)  # Sleep for 1 second
except KeyboardInterrupt:
    print("Exiting...")
    mqtt_client.disconnect()
