# docker build -t socket-server .
# docker run -d --name socket-server -p 5050:5050 socket-server

FROM python:3
LABEL description="Socket Server"
RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev
WORKDIR /app
COPY . .
#CMD ["python", "./app.py"]
CMD ["tail", "-f", "/dev/null"]