.PHONY: cov

build:
	docker-compose -f run.yml build
	docker-compose -f ddml/tests/peers/test_one_dead_peer.yml build

cov:
	# Generate coverage report
	poetry run pytest --cov-report html:cov_report --cov=.

format:
	# Re-format code to avoid IndentationErrors
	poetry run black ddml

clean:
	rm -rf cov_report dist .coverage*
	find ./ddml | grep __pycache__$ | xargs rm -rf
	find ./ | grep .pytest_cache$ | xargs rm -rf
