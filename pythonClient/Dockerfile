FROM python:3.8-slim
WORKDIR /usr/src/pythonserver
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8081
CMD ["python", "./flask-server/server.py"]
