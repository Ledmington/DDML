FROM python:alpine3.15
WORKDIR /home
COPY . /home
CMD python3 /home/peers/dead_peer.py