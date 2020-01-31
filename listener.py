# This part of the Chat application recieves the incoming messages and prints them

import paho.mqtt.client as mqtt

def run():

    #define constants
    #---

    host = "localhost"
    topic = "test/"

    username = "Test"
    password = None

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

    #define bahavior on events by passing the functions that should be called to the client
    #the functions are defined further down in the code
    #---

    mqtt_client.on_connect = behaviour_on_connect
    mqtt_client.on_subscribe = behaviour_on_subscribe
    mqtt_client.on_message = behaviour_on_message
    mqtt_client.on_disconnect = behaviour_on_disconnect

    #---

    #connect to the broker at the host address on the specified port
    mqtt_client.connect(host, port = 1883, keepalive = 30)

    #starts the main communication loop
    #from now on messages can be send
    mqtt_client.loop_start()

    #subscribes to a topic
    #from now on messages published on the topic will be send to the client
    #on recieving a message the client calls the on_message function
    mqtt_client.subscribe(topic, qos = 0)

    #now all messages are going to be displyed and we are waiting for user intup to end the program
    input("Press Enter to disconnect ... \n")

    #sending a good by message
    mqtt_client.publish(topic, payload = "User " + username + " disconnecting from " + topic + " .")

    #stopping the message loop
    mqtt_client.loop_stop()

    #disconnecting from the broker
    mqtt_client.disconnect()

    #now we are done and the program is going to end

#automaticly called on successfull connection
def behaviour_on_connect(client, userdata, flags, rc):
    print("Connection to the broker established.")

#automaticly called on successfull subscription
def behaviour_on_subscribe(client, userdata, mid, granted_qos):
    #we inform everyone subscribed to the topic that we are now also subscribed
    client.publish(userdata.get("topic"), payload = "User " + userdata.get("username") + " is now subscribed to " + userdata.get("topic") + " .")

#automaticly called on recieving a message
def behaviour_on_message(client, userdata, message):
    #the message recieved is a MQTT message clss with with the attributes topic, payload, qos and retain
    print(message.payload)

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
