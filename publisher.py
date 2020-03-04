# This part of the Chat application sends messages

import paho.mqtt.client as mqtt
import json

def run():

    #define constants
    #---

    host = "mothership.inf.tu-dresden.de"
    topic = "chat"

    username = "chat"
    password = "chat"

    #---

    #initialize the mqtt client that is going to handle all messages
    #user_info contains the basic information about the connection and is going to be returned to callbacks from the client
    user_info = {"host": host, "topic": topic, "username": username}
    mqtt_client = mqtt.Client(userdata = user_info)

    #optional define optional behaviour for the client
    #---

    #username and password used to connect to the broker
    mqtt_client.username_pw_set(username, password)
    #if the client disconnects without sending a proper disconnect this message will be puplished by the broker
    mqtt_client.will_set(topic, payload = "User " + username + " timed out.\n", qos = 0, retain = False)
    #specifies the time waited befor attempting to reconnect to the broker
    mqtt_client.reconnect_delay_set(min_delay=1, max_delay=120)

    #---

    #define the client bahavior by passing the functions that should be called to the client
    #the functions are defined further down in the code
    #---

    mqtt_client.on_connect = behaviour_on_connect
    mqtt_client.on_publish = behaviour_on_publish
    mqtt_client.on_disconnect = behaviour_on_disconnect

    #---

    #connect to the broker at the host address on the specified port
    mqtt_client.connect(host, port = 1883, keepalive = 30)

    #starts the main communication loop
    #from now on messages can be send
    mqtt_client.loop_start()

    #we want to program to continue until the user exits it
    running = True
    while running:

        #we ask the user for iput
        user_input = input("Enter your message. To exit the chat type exit.\n")

        #exit the loop if the user wants to
        if user_input == "exit" or user_input == "Exit":
            running = False

        #send the user input as a message
        else:
            #build the object to send as payload of the message
            payload = {"type": "message", "from": username, "message": user_input}
            #json.dumps transforms the dictionary into valid JSON
            #paho-mqtt cant send python dictionarys, but it can send JSON
            publish_status = mqtt_client.publish(topic, json.dumps(payload))

            #notice if sending the message failed for some reason
            #if you publish to a topic you have no write access to no error is going to be raised
            if publish_status.rc != mqtt.MQTT_ERR_SUCCESS:
                print("For some reason the message could not be sent.")


    #stopping the message loop
    mqtt_client.loop_stop()

    #disconnecting from the broker
    mqtt_client.disconnect()

    #now we are done and the program is going to end

#automaticly called after connection attempt
def behaviour_on_connect(client, userdata, flags, rc):

    #successfull connection
    if rc == 0:
        print("Connection to the broker established.")
    else:
        print("Connection failed.")
        sys.exit() #immediately end the program

#automaticly called when a message is successfully published
def behaviour_on_publish(client, userdata, mid):
    print("Message published")

#automaticly called if the client is disconnected from the server
def behaviour_on_disconnect(client, userdata, rc):

    #this is going to be the case if anything else that a disconnect on purpose occured
    if rc != 0:
        print("Unexpected disconnection!")

        #we should still stop the loop before termination the program
        client.loop_stop()

    else:
        print("Successfully dissconected!")

if __name__ == '__main__':
    run()
