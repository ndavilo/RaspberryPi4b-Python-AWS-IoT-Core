import boto3
import json
import ssl
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# AWS IoT Core Configuration
endpoint = "aa36isswp8ort-ats.iot.eu-west-3.amazonaws.com"
port = 8883
topic = "powersync/topic"

# Certificate and Keys
cert_path = "./6328a969b47f78572129bc50471a8d51d0f4bd2c4746d9689140575e183a5c3d-certificate.pem.crt"
key_path = "./6328a969b47f78572129bc50471a8d51d0f4bd2c4746d9689140575e183a5c3d-private.pem.key"
root_ca_path = "./root-CA.pem"

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

# Function to send message
def send_message(payload):
    mqtt_client.publish(topic, json.dumps(payload), 1)
    print("Message sent to AWS IoT Core:", payload)

# Function to handle incoming messages
def message_callback(client, userdata, message):
    print("Message received from AWS IoT Core:", message.payload.decode())

# Subscribe to the topic to receive messages
mqtt_client.subscribe(topic, 1, message_callback)

try:
    while True:
        # Send a message to AWS IoT Core every 5 minutes
        message = {"message": "Hello from Raspberry Pi4!"}
        send_message(message)
        time.sleep(300)  # Sleep for 5 minutes

except KeyboardInterrupt:
    print("Exiting...")
    mqtt_client.disconnect()
