FROM python:alpine3.15

# Installing poetry dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Installing poetry
RUN pip install poetry

# Copying all files
COPY . /home
WORKDIR /home

# Installing actual project dependencies
RUN poetry install --no-dev

# Cleaning up
RUN rm -rf /var/cache/apk/*

# Launching the normal peer
CMD poetry run python3 ddml/main.py