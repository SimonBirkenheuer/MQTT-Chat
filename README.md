# MQTT-Chat
A small MQTT based chat application

A project of mine to play with MQTT in python. Idea is to set up a small protocol and client to enable chatting in a chatroom based approach.

## WhyMQTT

MQTT is most likely not the most sensible choice for implementing a chat. The point of the project in to play around with MQTT though.

## How to start the MQTT Broker

### Arch Linux
After installing the mosquitto package simply run:

`mosquitto -c mosquitto.conf`

This should start a MQTT-Broker running on the default port 1883.<br>
The broker is configured to only accept connections from the user "Test" with the passworrd "test" and the user "Server" with the password "admin". Additionally this "Test" user is only allowed to read or write on the topic "test/" and all ist sub topics.<br>
You can manually interact with your new broker:

`mosquitto_sub -h localhost -t test/ -u Test -P test`<br>
*The topic for testing is aptly named test/.*

`mosquitto_pub -h localhost -t test/ -u Test -P test -m "Hello World"`<br>
*Publishes the message "Hello World" to the test/ topic. The message should now be recieved by the subscribed listener from above.*<br>

If you subscribe to a topic you do not have read access to you wont get a error you just wont get any messages.

For the RoboLab workshop the test user has the Username "chat" with password "chat" and access to topics starting with "chat".
The broker is hosted on mothership.inf.tu-dresden.de .

## How to start the application

Make sure you have the paho-mqtt and json python packages installed.<br>
To read the chat you have to start the listener.py.<br>
In order to send messages you have to start the publisher.py.<br>

Both programs allow for a host, topic and a username to be specified.

## About the chat protocol

MQTT allows us to transfer a payload. This Payload has to be a byte array like type. Internally the payload is represented as a python dictionary. This dictionary has to be converted in order to be transmitted. In this Project JSON is used for that purpose, since the json.dumps() and json.loads() methods from the json package for python allow for easy conversion.

The messages have multiple fields:

"type": Either "message" or "notice"<br>
"from": Username of the author<br>
"message": Only present if "type" is "message", contains the message string<br>
"notice": Only present if "type" is "info", contains a string description<br>

## Misc

Documentation of the paho mqtt library for python
[https://www.eclipse.org/paho/clients/python/docs/#client]
