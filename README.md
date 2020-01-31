# MQTT-Chat
A small MQTT based chat application

A project of mine to play with MQTT in python. Idea is to set up a small protocol and client to enable chatting in a chatroom based approach.

## WhyMQTT

MQTT is most likely not the most sensible choice for implementing a chat. The point of the project in to play around with MQTT though.

## How to start the MQTT Broker

### Arch Linux
After installing the mosquitto package simply run:

`mosquitto`

This should start a MQTT-Broker running on the default port 1883.<br>
You can manually interact with your new broker:

`mosquitto_sub -h localhost -t test/`<br>
*The topic for testing is aptly named test/.*

`mosquitto_pub -h localhost -t test/ -m "Hello World"`<br>
*Publishes the message "Hello World" to the test/ topic. The message should now be recieved by the subscribed listener from above.*

## How to start the application

Make sure you have the paho-mqtt python package installed.<br>
To start the listener simply run listener.py.

## About the chat protocol

MQTT allows us to transfer a payload. This Payload has to be a byte array like type. Internaly the payload is represented as a python dictionary. This dictionary has to be converted in order to be transmitted. In this Project JSON is used for that purpose, since the json.dumps() and json.loads() methods from the json package for python allow for easy conversion.

The messages have multiple fields:

"type": Either "message" or "info"
"from": Username of the author
"message": only present if "type" is "message", contains the message string

## Misc

Documentation of the paho mqtt library for python
[https://www.eclipse.org/paho/clients/python/docs/#client]
