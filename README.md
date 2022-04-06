# Decentralized Distributed Machine Learning
Train ML models in a distributed and decentralized manner.

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

To run a specific test file, run:
```
poetry run pytest path/to/test/file.py
```