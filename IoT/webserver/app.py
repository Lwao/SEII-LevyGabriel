from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from flask_mqtt import Mqtt

app = Flask(__name__)

port1_status = 'offline'
port2_status = 'offline'
port3_status = 'offline'
port4_status = 'offline'
port5_status = 'offline'


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

@mqtt.on_connect()
def handle_mqtt_connect(client, userdata, flags, rc):
    if rc == 0:
        USERS = ['blue']
        
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

    global port1_status, port2_status, port3_status, port4_status, port5_status

    print("Received message: " + data['topic'] + " -> " + data['payload'])

    topic = data['topic'].split("/") # split message topic
    tlen = len(topic) # topic length

    if tlen>=1: username = topic[1] # user is the first input
    if tlen==3: # status command
        if topic[2]=='status':
            ###### upload availability status to db
            if data['payload']=='online': # if online sends all ports values for given user
                ###### fetch all port data from the db for current user
                for port in range(1,16): mqtt.publish(f"trabalho_final_2_iot/%s/devices/port%d" % (username,port), "off", 2) # initialize ports to user based in db data
    if tlen==4: # devices command
        if topic[2]=='devices': 
            ###### must forward the port's online/offline status to the db 
            port = topic[3] # store port
            if port=='port1': port1_status = data['payload']
            elif port=='port2': port2_status = data['payload']
            elif port=='port3': port3_status = data['payload']
            elif port=='port4': port4_status = data['payload']
            elif port=='port5': port5_status = data['payload']
                            
    

@app.route('/', methods=['POST', 'GET'])
def control_route():
    return render_template('dashboard.html')

@app.route('/handle_devices', methods=['POST'])
def handle_devices():
    port1 = request.form["port1"]
    port2 = request.form["port2"]
    port3 = request.form["port3"]
    port4 = request.form["port4"]
    port5 = request.form["port5"]

    if port1=='on' or port1=='off': mqtt.publish(f"trabalho_final_2_iot/%s/devices/port1" % ('blue'), port1, 2)
    if port2=='on' or port2=='off': mqtt.publish(f"trabalho_final_2_iot/%s/devices/port2" % ('blue'), port2, 2)
    if port3=='on' or port3=='off': mqtt.publish(f"trabalho_final_2_iot/%s/devices/port3" % ('blue'), port3, 2)
    if port4=='on' or port4=='off': mqtt.publish(f"trabalho_final_2_iot/%s/devices/port4" % ('blue'), port4, 2)
    if port5=='on' or port5=='off': mqtt.publish(f"trabalho_final_2_iot/%s/devices/port5" % ('blue'), port5, 2)

    return '', 204

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    # db.init_app(app)
    # mqtt.init_app(app)