FROM python:alpine3.15

# Upgrading packets
RUN apk update
RUN apk upgrade

# Upgrading pip
RUN python3 -m pip install --upgrade pip

# Installing poetry dependencies
RUN apk add gcc musl-dev libffi-dev

# Installing poetry
RUN pip install poetry

# Copying all files
COPY . /home
WORKDIR /home

# Installing actual project dependencies
RUN poetry install

# Launching the normal peer
CMD poetry run python3 ddml/peers/normal/normal_peer.py