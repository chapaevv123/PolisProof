.PHONY: run test eval eval-live demo-artifacts validate

run:
	docker compose up --build

test:
	docker build --target test -t polisproof-test .

eval:
	docker build --target eval -t polisproof-eval .

eval-live:
	python evaluation/live_benchmark.py

demo-artifacts:
	python evaluation/export_demo.py

validate: demo-artifacts
	python evaluation/validate_artifacts.py
