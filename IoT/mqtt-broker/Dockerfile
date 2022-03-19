# docker build -t mosquitto-broker .
# docker run -d --name mosquitto-broker -p 1883:1883 mosquitto-broker

FROM eclipse-mosquitto:latest
LABEL description="Eclipse Mosquitto MQTT Broker"
VOLUME ["/mosquitto/data", "/mosquitto/log","/mosquitto/config"]
COPY /mosquitto/config/mosquitto.conf /mosquitto/config/
EXPOSE 1883