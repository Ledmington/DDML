# Decentralized Distributed Machine Learning
![example workflow](https://github.com/Ledmington/DDML/actions/workflows/main.yml/badge.svg)

Train ML models in a distributed and decentralized manner.

## Instructions
### Running the Docker container
You can run the peer packaged inside a docker container with:
```bash
docker run -it --rm filippobarbari/ddml-peer
```

### Run standalone
**TODO**

## Local development
For local development, you'll need `poetry` installed. You can do it with:
```
pip install poetry
```

### Install dependencies
The first time, you'll need to let `poetry` install the project dependencies for you. To do so, run:
```
poetry install
```
from the root directory of the project.

### Run tests
To run all tests, simply run `make` or `make cov` from the root directory of the project, these commands will generate an HTML coverage report.
You can view it from `./cov_report/index.html`.

Running all tests at once, including those in the `ddml/tests/peers/integration` folder, can take quite a long time. To shorten this time (and to debug easily, if needed), run `make build` before `make cov`. With this command, the container images needed for the integration testing are built and stored.

To run a specific test file, run:
```
poetry run pytest path/to/test/file.py
```