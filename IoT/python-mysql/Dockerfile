# docker build -t python-mysql .
# docker run -d --name python-mysql -p 5050:5050 python-mysql

FROM python:3
LABEL description="Python MySQL test"
RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev
WORKDIR /app
RUN pip install mysql-connector-python
COPY . .
#CMD ["python", "./app.py"]
CMD ["tail", "-f", "/dev/null"]