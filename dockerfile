FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN pip install Pillow

EXPOSE 8000

CMD [ "python", "server.py" ]
