build:
	docker-compose -f run.yml build
	docker-compose -f ddml/tests/peers/test_one_dead_peer.yml build

cov:
	# Generate coverage report
	poetry run pytest --cov-report html:cov_report --cov=.

	# Open coverage report with default browser
	open cov_report/index.html 2>/dev/null

clean:
	rm -rf cov_report dist .coverage* **/__pycache__ **/.pytest_cache