.PHONY: test test-verbose test-cov test-unit test-integration help install-dev clean

# Default target
help:
	@echo "Available targets:"
	@echo "  make test              - Run all tests using .venv"
	@echo "  make test-verbose      - Run tests with verbose output"
	@echo "  make test-cov          - Run tests with coverage report"
	@echo "  make test-unit         - Run only unit tests"
	@echo "  make test-integration  - Run only integration tests"
	@echo "  make install-dev       - Install package in development mode with test dependencies"
	@echo "  make clean             - Clean build artifacts"

# Run all tests using .venv
test:
	@./run_tests.sh

# Run tests with verbose output
test-verbose:
	@./run_tests.sh -v

# Run tests with coverage
test-cov:
	@./run_tests.sh --cov=chpy --cov-report=html --cov-report=term

# Run only unit tests
test-unit:
	@./run_tests.sh -m unit

# Run only integration tests
test-integration:
	@./run_tests.sh -m integration

# Install package in development mode
install-dev:
	@if [ ! -d ".venv" ]; then \
		echo "Creating .venv..."; \
		python3 -m venv .venv; \
	fi
	@.venv/bin/pip install -e .
	@.venv/bin/pip install pytest pytest-cov

# Clean build artifacts
clean:
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -rf htmlcov/
	@rm -rf .pytest_cache/
	@rm -rf .coverage
	@find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true

