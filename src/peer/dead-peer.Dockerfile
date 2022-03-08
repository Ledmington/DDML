FROM python:alpine3.15
WORKDIR /home
COPY peer.py /home
COPY dead-peer.py /home
CMD python3 dead-peer.py