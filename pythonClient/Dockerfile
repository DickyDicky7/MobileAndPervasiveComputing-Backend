FROM python:3.8-slim
WORKDIR /usr/src/pythonserver
COPY . .
RUN pip install --no-cache-dir flask transformers pillow requests pytesseract tensorflow
EXPOSE 8081
CMD ["python", "./flask-server/server.py"]
