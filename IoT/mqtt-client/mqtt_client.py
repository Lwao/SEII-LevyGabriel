import paho.mqtt.client as mqtt

# data to fetch in the database
"""
Must load the current available users and fetch their data in the db
"""
USERS = ['red','blue','green']

connected = False # connection status
msgReceived = False # message status

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        # print("Connected successfully")
        global connected
        connected=True

        # subscribe to all users main topics
        for username in USERS: 
            client.subscribe(f"%s/#" % username, 2) # subscribe to desired topics with QoS level 2
            client.publish(f"%s/status" % username, "offline") # try to publish offline status to all housenodes
    else:
        # None
        print("Connect returned result code: " + str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, obj, msg):
    print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))

    payload = msg.payload.decode("utf-8") # decode payload
    topic = msg.topic.split("/") # split message topic
    
    tlen = len(topic) # topic length
    if tlen>=1: username = topic[0] # user is the first input
    if tlen==2: # status command
        if topic[1]=='status':
            """
            Upload availability status to db
            """
            if payload=='online': # if online sends all ports values for given user
                """
                Fetch all port data from the db
                """
                for port in range(1,16): client.publish(f"%s/devices/port%d" % (username,port), "online") # initialize ports to user based in db data
    if tlen==3: # devices command
        if topic[1]=='devices': 
            port = topic[2] # store port
            """
            Must forward the port's online/offline status to the db and inform the webserver
            """

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

def start_mqtt_client():
    # connection credentials
    brokerAddress = "mosquitto-broker-app" # broker address
    port = 1883 # TCP/IP port
    userName = "" # server username
    passWord = "" # server password

    # mqtt client configuration
    client = mqtt.Client("Dashboard") # create the mqtt client
    client.on_connect = on_connect # set on connect callback
    client.on_message = on_message # set on message callback
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.username_pw_set(userName, passWord) # set username and password
    client.connect(brokerAddress, port) # connect to mosquitto broker on port 1883
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS) # enable TLS
    #client.on_log = on_log # uncomment to enable debug messages

    # Continue the network loop, exit when an error occurs
    rc = 0
    while rc == 0:
        rc = client.loop()
    print("rc: " + str(rc))

if __name__ == "__main__":
    start_mqtt_client()