import paho.mqtt.client as mqtt
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        # print("Connected successfully")
        global connected
        connected=True
    else:
        # None
        print("Connect returned result code: " + str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, obj, msg):
    print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))
    # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

connected = False # connection status
msgReceived = False # message status

brokerAddress = "localhost" # broker address
port = 1883 # TCP/IP port
userName = "mqtt" # server username
passWord = "password" # server password

# mqtt client configuration
client = mqtt.Client("Dashboard") # create the mqtt client
client.on_connect = on_connect # set on connect callback
client.on_message = on_message # set on message callback
client.on_publish = on_publish
client.on_subscribe = on_subscribe
#client.on_log = on_log # uncomment to enable debug messages
client.username_pw_set(userName, passWord) # set username and password
client.connect(brokerAddress, port) # connect to mosquitto broker on port 1883
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS) # enable TLS

client.subscribe("/", 0) # subscribe to desired topics with QoS level 0
client.publish("/", "Hello Mosquitto!") # Publish a message

# Continue the network loop, exit when an error occurs
rc = 0
while rc == 0:
    rc = client.loop()
print("rc: " + str(rc))

# client.loop_start()

# while connected!=True:
#     time.sleep(0.2)
# while msgReceived!=True:
#     time.sleep(0.2)


# client.loop_stop()