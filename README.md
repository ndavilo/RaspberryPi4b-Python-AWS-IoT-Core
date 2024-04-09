# Raspberry Pi AWS IoT Core Communication

This project demonstrates bidirectional communication between a Raspberry Pi and AWS IoT Core. The Raspberry Pi runs on Raspberry Pi OS and utilizes Python code for communication.

## Features

- Establishes bidirectional communication with AWS IoT Core.
- Uses TLS encryption for secure data transmission.
- Authenticates using X.509 certificates.
- Controls devices via GPIOZero library.
- Facilitates message exchange using the MQTT protocol.

## Prerequisites

- Raspberry Pi running Raspberry Pi OS.
- AWS IoT Core account with necessary configurations.
- Python 3.x installed on the Raspberry Pi.
- Required Python packages installed (see `requirements.txt`).

## Usage

1. Clone this repository to your Raspberry Pi.
2. Install required Python packages using `pip install -r requirements.txt`.
3. Configure the `.env` file with your AWS IoT Core credentials and paths to certificate files.
4. Run the Python script `raspberry_pi_aws_iot.py`.
5. Monitor the console for incoming messages and device control actions.

## Configuration

Configure the `.env` file with the following AWS IoT Core settings:

```dotenv
# AWS IoT Core Configuration
ENDPOINT="your_aws_iot_endpoint"
PORT=8883
TOPIC="your_topic"

# Certificate and Keys
CERT_PATH="./path/to/certificate.pem.crt"
KEY_PATH="./path/to/private.pem.key"
ROOT_CA_PATH="./path/to/root-CA.pem"
