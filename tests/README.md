# chpy Test Suite

Comprehensive pytest test suite for the chpy library, covering all major components and functionality.

## Test Structure

The test suite is organized into logical modules:

- **`conftest.py`** - Pytest fixtures, configuration, and shared test utilities
- **`test_client.py`** - Tests for `ClickHouseClient` connection and query execution
- **`test_orm.py`** - Tests for ORM classes (`Column`, `ColumnExpression`, `CombinedExpression`, `Table`, `Row`, `Subquery`)
- **`test_query_builder.py`** - Tests for `QueryBuilder` fluent interface and method chaining
- **`test_functions.py`** - Tests for function classes (`Function`, `AggregateFunction`, `WindowSpec`) and function factories
- **`test_schema.py`** - Tests for schema definitions and table schemas
- **`test_tables.py`** - Tests for table wrappers (`CryptoQuotesTable`, `TableWrapper`)
- **`test_config.py`** - Tests for configuration constants and helper functions
- **`test_ddl.py`** - Tests for DDL operations (CREATE, ALTER, DROP tables/databases)
- **`test_types.py`** - Tests for ClickHouse type builders (Array, Map, Tuple, Nested, etc.)
- **`test_integration.py`** - Integration tests combining multiple components in real-world scenarios

## Running Tests

### Basic Commands

#### Run all tests
```bash
pytest
```

#### Run with verbose output
```bash
pytest -v
```

#### Run with extra verbose output (shows print statements)
```bash
pytest -v -s
```

#### Run specific test file
```bash
pytest tests/test_client.py
```

#### Run specific test class
```bash
pytest tests/test_client.py::TestClickHouseClient
```

#### Run specific test function
```bash
pytest tests/test_client.py::TestClickHouseClient::test_init_defaults
```

#### Run tests matching a pattern
```bash
pytest -k "test_query"  # Run all tests with "query" in the name
pytest -k "test_orm or test_client"  # Run tests matching either pattern
```

### Advanced Options

#### Run with coverage report
```bash
# First install pytest-cov: pip install pytest-cov
pytest --cov=chpy --cov-report=html
```

This generates an HTML coverage report in `htmlcov/index.html`.

#### Run with coverage and show missing lines
```bash
pytest --cov=chpy --cov-report=term-missing
```

#### Run only fast tests (skip slow/integration tests)
```bash
pytest -m "not slow"
```

#### Run tests in parallel (requires pytest-xdist)
```bash
pip install pytest-xdist
pytest -n auto  # Use all CPU cores
pytest -n 4     # Use 4 workers
```

#### Stop on first failure
```bash
pytest -x
```

#### Stop after N failures
```bash
pytest --maxfail=3
```

#### Show local variables on failure
```bash
pytest -l
```

#### Run tests with warnings as errors
```bash
pytest -W error
```

### Test Markers

The test suite uses pytest markers for categorization:

- `@pytest.mark.slow` - Mark slow-running tests
- `@pytest.mark.integration` - Mark integration tests
- `@pytest.mark.unit` - Mark unit tests

Run tests by marker:
```bash
pytest -m unit          # Run only unit tests
pytest -m "not slow"    # Skip slow tests
pytest -m integration   # Run only integration tests
```

## Test Coverage

The test suite provides comprehensive coverage of:

### ✅ Core Components

- **ClickHouseClient**
  - Connection initialization with various parameters
  - Query execution (SELECT, INSERT, commands)
  - Multiple output formats (list, DataFrame, NumPy, Arrow)
  - Context manager support
  - Error handling

- **ORM Classes**
  - `Column` - Column definition and type handling
  - `ColumnExpression` - Expression building (==, !=, <, >, IN, NOT IN, LIKE)
  - `CombinedExpression` - AND/OR combinations
  - `Table` - Table schema definition
  - `Row` - Row object with attribute and dictionary access
  - `Subquery` - Subquery support for WHERE, SELECT, FROM clauses
  - `SubqueryExpression` - EXISTS/NOT EXISTS expressions

- **QueryBuilder**
  - Method chaining and fluent interface
  - SELECT clause with columns, functions, subqueries
  - WHERE conditions (column expressions, raw SQL, subqueries)
  - JOIN operations (INNER, LEFT, RIGHT, FULL, CROSS)
  - GROUP BY and HAVING clauses
  - ORDER BY with ascending/descending
  - LIMIT clause
  - Multiple output formats (list, dict, DataFrame, NumPy, JSON, CSV, Parquet)
  - Count, first, exists methods
  - Iteration support

- **Functions**
  - Base `Function` class
  - `AggregateFunction` class
  - `WindowSpec` for window functions
  - Function factories for all ClickHouse functions
  - Alias support
  - OVER clause support for window functions

- **Table Wrappers**
  - `TableWrapper` - Generic table wrapper
  - `CryptoQuotesTable` - Specialized crypto quotes wrapper
  - Schema-based type safety
  - Helper methods for exchanges and pairs

- **DDL Operations**
  - CREATE TABLE with various engines and options
  - ALTER TABLE (add, drop, modify columns)
  - DROP TABLE
  - RENAME TABLE
  - CREATE/DROP DATABASE
  - CREATE/DROP MATERIALIZED VIEW
  - CREATE DISTRIBUTED TABLE

- **Type System**
  - Basic types (String, Int64, Float64, etc.)
  - Complex types (Array, Map, Tuple, Nested)
  - Type modifiers (Nullable, LowCardinality)
  - Special types (IPv4, IPv6, UUID, Date, DateTime, DateTime64)
  - FixedString and Enum types
  - Convenience functions (LowCardinalityNullable, etc.)

- **Configuration**
  - Exchange constants
  - Currency mappings
  - Pair validation helpers
  - Exchange-specific pair generation

### ✅ Integration Scenarios

- End-to-end query building and execution
- Complex queries with multiple clauses
- JOIN operations with multiple tables
- Window functions with various specifications
- Subqueries in different contexts
- DDL operations followed by queries
- Type system usage in table creation

## Writing Tests

### Test File Structure

```python
import pytest
from chpy import ClickHouseClient, CryptoQuotesTable
from chpy.orm import Table, Column

class TestMyFeature:
    """Test class for my feature."""
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        # Arrange
        client = ClickHouseClient(...)
        table = CryptoQuotesTable(client)
        
        # Act
        result = table.query().where(...).to_list()
        
        # Assert
        assert len(result) > 0
        assert result[0]['pair'] == "BTC-USDT"
    
    def test_edge_case(self):
        """Test edge case."""
        # Test implementation
        pass
    
    @pytest.mark.slow
    def test_slow_operation(self):
        """Test slow operation."""
        # Test implementation
        pass
```

### Using Fixtures

The test suite provides fixtures in `conftest.py`:

```python
def test_with_fixture(mock_client):
    """Test using a fixture."""
    # mock_client is automatically provided
    result = mock_client.execute("SELECT 1")
    assert result == [{"1": 1}]
```

### Mocking ClickHouse

Tests use mocks to avoid requiring a live database connection:

```python
from unittest.mock import Mock, MagicMock

def test_query_execution(mock_client):
    """Test query execution with mocked client."""
    # The mock_client fixture provides a mocked ClickHouse client
    table = CryptoQuotesTable(mock_client)
    result = table.query().to_list()
    # Assertions...
```

### Testing Error Cases

```python
def test_error_handling():
    """Test error handling."""
    with pytest.raises(ValueError):
        # Code that should raise ValueError
        invalid_operation()
    
    with pytest.raises(ConnectionError, match="Failed to connect"):
        # Code that should raise ConnectionError with specific message
        ClickHouseClient(host="invalid")
```

### Testing Async/Context Managers

```python
def test_context_manager():
    """Test context manager usage."""
    with ClickHouseClient(...) as client:
        table = CryptoQuotesTable(client)
        result = table.query().to_list()
        assert result is not None
    # Connection should be closed after context exit
```

## Test Best Practices

### 1. Test Isolation

Each test should be independent and not rely on other tests:

```python
# Good: Each test is independent
def test_query_1():
    client = ClickHouseClient(...)
    # Test implementation

def test_query_2():
    client = ClickHouseClient(...)
    # Test implementation

# Avoid: Tests that depend on each other
def test_create_table():
    # Creates table

def test_query_table():
    # Assumes table from previous test exists
```

### 2. Use Descriptive Test Names

```python
# Good: Descriptive names
def test_query_with_multiple_where_clauses():
    pass

def test_join_with_table_alias():
    pass

# Avoid: Vague names
def test_query():
    pass

def test_join():
    pass
```

### 3. Test Both Success and Failure Cases

```python
def test_valid_input():
    """Test with valid input."""
    result = function(valid_input)
    assert result is not None

def test_invalid_input():
    """Test with invalid input."""
    with pytest.raises(ValueError):
        function(invalid_input)
```

### 4. Use Parametrized Tests for Multiple Cases

```python
@pytest.mark.parametrize("pair,expected_count", [
    ("BTC-USDT", 100),
    ("ETH-USDT", 50),
    ("BNB-USDT", 25),
])
def test_query_by_pair(pair, expected_count):
    """Test querying by different pairs."""
    result = table.query().where(crypto_quotes.pair == pair).count()
    assert result == expected_count
```

### 5. Test Edge Cases

```python
def test_empty_result():
    """Test query with no results."""
    result = table.query().where(crypto_quotes.pair == "NONEXISTENT").to_list()
    assert result == []

def test_null_handling():
    """Test handling of NULL values."""
    # Test implementation
    pass
```

## Continuous Integration

The test suite is designed to run in CI/CD environments:

```yaml
# Example GitHub Actions workflow
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-cov
      - run: pytest --cov=chpy --cov-report=xml
      - uses: codecov/codecov-action@v2
```

## Debugging Tests

### Run with Debugger

```bash
# Use Python debugger
pytest --pdb

# Drop into debugger on failure
pytest --pdb --pdbcls=IPython.terminal.debugger:Pdb
```

### Print Debug Information

```python
def test_with_debug():
    result = table.query().to_list()
    print(f"Debug: Found {len(result)} results")
    print(f"Debug: First result: {result[0] if result else None}")
    assert len(result) > 0
```

### Use Logging

```python
import logging

def test_with_logging(caplog):
    """Test with logging capture."""
    with caplog.at_level(logging.DEBUG):
        result = table.query().to_list()
        assert "Query executed" in caplog.text
```

## Performance Testing

For performance-critical code, add performance tests:

```python
import time

@pytest.mark.slow
def test_query_performance():
    """Test query performance."""
    start = time.time()
    result = table.query().limit(10000).to_list()
    duration = time.time() - start
    
    assert duration < 1.0  # Should complete in under 1 second
    assert len(result) == 10000
```

## Notes

- Tests use mocks for ClickHouse client to avoid requiring a live database connection
- All tests are designed to run quickly and independently
- Integration tests demonstrate real-world usage patterns
- The test suite is continuously expanded to cover new features and edge cases

## Contributing Tests

When adding new features, please:

1. Add corresponding tests in the appropriate test file
2. Ensure tests pass with `pytest`
3. Maintain or improve test coverage
4. Follow existing test patterns and conventions
5. Add docstrings to test functions explaining what they test

## Questions?

For questions about the test suite, please open an issue on GitHub.
