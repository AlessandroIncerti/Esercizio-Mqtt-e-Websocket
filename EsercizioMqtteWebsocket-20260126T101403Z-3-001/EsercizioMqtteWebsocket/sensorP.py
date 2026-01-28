import datetime
import time
import random
import json
import paho.mqtt.client as mqtt

BROKER = "mqtt.ssh.edu.it"     # test.mosquitto.org
TOPIC = "Incerti/sensor/pressure"

client = mqtt.Client()
client.connect(BROKER, 1883)

print("Sensore simulato avviato")

while True:
    value = round(random.uniform(18, 30), 2)

    payload = {
        "sensor": "pressure",
        "valore": value,
        "unit": "bar",
        "timestamp": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    client.publish(TOPIC, json.dumps(payload))
    print("Pubblicato:", payload)

    time.sleep(1)
