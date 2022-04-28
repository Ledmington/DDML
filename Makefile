RUN=poetry run

.PHONY: cov

build:
	docker-compose -f run.yml build
	docker-compose -f ddml/tests/peers/integration/test_one_dead_peer.yml build

cov:
	# Generate coverage report
	${RUN} pytest --cov-report html:cov_report --cov=./ddml ./ddml/tests

format:
	# Re-format code to avoid IndentationErrors
	${RUN} black ddml

mut:
	# Run full mutation testing
	${RUN} mutmut run

run:
	${RUN} python3 ddml/main.py

interactive:
	${RUN} python3 ddml/main.py -i

check:
	${RUN} pylint ddml

clean:
	rm -rf cov_report dist .coverage .idea
	find ./ddml | grep __pycache__$ | xargs rm -rf
	find ./ | grep .pytest_cache$ | xargs rm -rf
