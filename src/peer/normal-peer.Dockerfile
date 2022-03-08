FROM python:alpine3.15
WORKDIR /home
COPY peer.py /home
COPY normal-peer.py /home
CMD python3 normal-peer.py