# docker build -t paho-client .
# docker run -d --name paho-client -p 1883:1883 paho-client

FROM python:3
LABEL description="Paho MQTT Client"
RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev
WORKDIR /app
RUN pip install paho-mqtt
COPY . .
#CMD ["python", "./app.py"]
CMD ["tail", "-f", "/dev/null"]