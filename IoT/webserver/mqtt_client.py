import paho.mqtt.client as mqtt
import time

connected = False # connection status
msgReceived = False # message status

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        # print("Connected successfully")
        global connected
        connected=True

        ###### get USER list from db
        USERS = ['red','blue','green']
        
        for username in USERS: # subscribe to all users main topics
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

    obj['pipe'].send(msg.topic) # beacons that the given topic was updated

    if tlen>=1: username = topic[0] # user is the first input
    if tlen==2: # status command
        if topic[1]=='status':
            ###### upload availability status to db
            if payload=='online': # if online sends all ports values for given user
                ###### fetch all port data from the db for current user
                for port in range(1,16): client.publish(f"%s/devices/port%d" % (username,port), "online") # initialize ports to user based in db data
    if tlen==3: # devices command
        if topic[1]=='devices': 
            ###### must forward the port's online/offline status to the db 
            port = topic[2] # store port
            

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

def handle_command(cmd):
    header, body = cmd.split(':')

    if header=='topic': # topic updated
        ###### fetch db for topic data
        ###### publish data from db to housenode
        pass
    if header=='user': # new user
        if body=='update':
            ###### fetch db for all user
            ###### fetch db for all user port data
            ###### publish all user port data to housenode
            pass


def start_mqtt_client(conn):
    # connection credentials
    brokerAddress = "mosquitto-broker-app" # broker address
    port = 1883 # TCP/IP port
    userName = "" # server username
    passWord = "" # server password

    # mqtt client configuration
    userdata_dict = {'pipe': conn}
    client = mqtt.Client(userdata=userdata_dict) # create the mqtt client
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
        # handle incoming messages from Flask webserver
        if conn.poll(timeout=.1): 
            msg = conn.recv()
            if msg: 
                print('MQTT client -> ' + msg)
                handle_command(msg)
        # proceeds with mqtt loop
        rc = client.loop()
        time.sleep(.01)
    print("rc: " + str(rc))

if __name__ == "__main__":
    start_mqtt_client()