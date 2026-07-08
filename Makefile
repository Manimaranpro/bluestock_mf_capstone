load:
	python src/etl/loader.py

ratios:
	python src/analytics/performance.py

test:
	pytest tests/

report:
	python src/reports/generate_report.py

dashboard:
	python src/dashboard/run_dashboard.py

api:
	python src/api/fetch_prices.py

clean:
	rm -rf __pycache__ .pytest_cache
