FROM ubuntu:latest

# Upgrading packets
RUN apt update -y
RUN apt upgrade -y
RUN apt install software-properties-common -y
RUN apt autoremove -y
RUN apt autoclean -y
RUN apt clean -y

RUN apt install python3 -y
RUN apt install python3-pip -y

# Installing poetry dependencies
#RUN apk add gcc musl-dev libffi-dev

# Installing poetry
RUN pip install poetry

RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update -y
RUN apt install python3.9 -y

# Copying all files
COPY . /home
WORKDIR /home

# Installing actual project dependencies
RUN poetry install

# Launching the normal peer
CMD poetry run pytest