sources = src/ tests/

.PHONY: run
run:
	uvicorn src.dusa_backend.main:app --reload

.PHONY: install-dev
install-dev:
	poetry install --with dev

.PHONY: format
format:
	poetry run ruff format $(sources)

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: test
test:
	poetry run pytest --cov=src --cov-report=xml # --cov-fail-under=100

.PHONY: cov-report
cov-report:
	poetry run pytest --cov=src --cov-report=html

.PHONY: start-dev-docker
start-dev-docker:
	@docker-compose -f docker/docker-compose.dev.yaml up -d

.PHONY: stop-dev-docker
stop-dev-docker:
	@docker-compose -f docker/docker-compose.dev.yaml down

.PHONY: start-test-docker
start-test-docker:
	@docker-compose -f docker/docker-compose.testing.yaml up -d

.PHONY: stop-test-docker
stop-test-docker:
	@docker-compose -f docker/docker-compose.testing.yaml down
