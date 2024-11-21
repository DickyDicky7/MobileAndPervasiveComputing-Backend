FROM python:3.8-slim
WORKDIR /usr/src/pythonserver
COPY . .
RUN apt-get update
RUN apt-get install -y tesseract-ocr
RUN apt-get   clean
RUN rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r ./flask-server/requirements.txt
# RUN pip install --no-binary=h5py h5py
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
EXPOSE 27018
CMD ["python", "./flask-server/server.py"]
