# docker build -t flask-webserver .
# docker run -d --name flask-webserver -p 1883:1883 flask-webserver

FROM python:3
LABEL description="Flask Webserver"
RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev
WORKDIR /app
RUN pip install flask Flask-SQLAlchemy flask-mqtt flask-login
COPY . .
EXPOSE 5000
#CMD ["python", "./app.py"]
CMD ["tail", "-f", "/dev/null"]