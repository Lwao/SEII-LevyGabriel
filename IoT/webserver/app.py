from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mqtt import Mqtt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_CLEAN_SESSION'] = True
app.config['MQTT_CLIENT_ID'] = 'iot-client-seII'
app.config['MQTT_LAST_WILL_TOPIC'] = 'server'
app.config['MQTT_LAST_WILL_MESSAGE'] = 'offline'
app.config['MQTT_LAST_WILL_QOS'] = 0

mqtt = Mqtt(app)
db = SQLAlchemy(app)

# class Devices(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30))
#     state = db.Column(db.String(10))

#     def __init__(self, id, name, state):
#         self.id = id
#         self.name = name
#         self.state = state

# device = Devices.query.filter_by(id=1).first()


@mqtt.on_connect()
def handle_mqtt_connect(client, userdata, flags, rc):
    if rc == 0:
        ###### get USER list from db
        USERS = ['red','blue','green']
        
        for username in USERS: # subscribe to all users main topics
            mqtt.subscribe(f"trabalho_final_2_iot/%s/#" % username, 2) # subscribe to desired topics with QoS level 2
            mqtt.publish(f"trabalho_final_2_iot/%s/status" % username, "offline", 2) # try to publish offline status to all housenodes
        
        mqtt.publish('trabalho_final_2_iot/server', 'online', 2) # server is online
        print("Connected successfully")
    else:
        # None
        print("Connect returned result code: " + str(rc))

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode("utf-8")
    )

    print("Received message: " + data['topic'] + " -> " + data['payload'])

    
    topic = data['topic'].split("/") # split message topic
    tlen = len(topic) # topic length

    if tlen>=1: username = topic[1] # user is the first input
    if tlen==3: # status command
        if topic[2]=='status':
            ###### upload availability status to db
            if data['payload']=='online': # if online sends all ports values for given user
                ###### fetch all port data from the db for current user
                for port in range(1,16): mqtt.publish(f"trabalho_final_2_iot/%s/devices/port%d" % (username,port), "online", 2) # initialize ports to user based in db data
    if tlen==4: # devices command
        if topic[2]=='devices': 
            ###### must forward the port's online/offline status to the db 
            port = topic[3] # store port
    

@app.route('/', methods=['POST', 'GET'])
def control_route():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    # db.init_app(app)
    # mqtt.init_app(app)