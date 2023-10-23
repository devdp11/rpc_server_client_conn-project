FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install Pillow

CMD [ "python", "server.py" ]
