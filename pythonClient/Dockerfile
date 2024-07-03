FROM python:3.8-slim
WORKDIR /usr/src/pythonserver
COPY . .
RUN pip3 install --no-cache-dir -r ./flask-server/requirements.txt
RUN pip3 install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
EXPOSE 27018
CMD ["python", "./flask-server/server.py"]
