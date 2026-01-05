#!/usr/bin/env python3
"""
Comprehensive examples demonstrating the chpy library with ORM-style column objects.
All queries use column objects for type safety and autocomplete support.

Run interactively:
    python example.py

Run specific example:
    python example.py --example 1

Run all examples:
    python example.py --all

List all examples:
    python example.py --list
"""

from chpy import ClickHouseClient, CryptoQuotesTable, crypto_quotes, avg, count, min, max, sum
from chpy.functions import (
    # String functions
    length, upper, lower, substring, concat, startsWith, endsWith,
    replace, replaceAll, splitByChar, reverse, trimBoth, left, right,
    position, extractAll, format, formatReadableQuantity, base64Encode, base64Decode,
    # Date/time functions
    toYear, toMonth, toDayOfMonth, toHour, addDays, subtractDays, now, today,
    toStartOfDay, toStartOfHour, toStartOfMonth, toStartOfYear,
    toMinute, toSecond, toDayOfWeek, toQuarter,
    dateDiff, addHours, subtractHours, addMinutes, formatDateTime,
    # Math functions
    abs, sqrt, round, floor, ceil, divide, plus, minus, multiply,
    log, log2, log10, exp, pow, power, sin, cos, tan, asin, acos, atan,
    # Type conversion
    toString, toInt64, toFloat64, toDateTime, toDate,
    # Conditional
    if_ as if_func, coalesce, multiIf, ifNull, nullIf,
    # Array functions
    array, arraySum, arrayAvg, arrayMax, arrayMin, arrayConcat, arrayElement,
    has, hasAll, hasAny, indexOf, countEqual, arraySort, arrayReverse,
    arraySlice, arrayJoin, arrayFilter, arrayMap, arrayCount, arrayDistinct,
    # Aggregate functions
    quantile, quantileExact, stddevPop, stddevSamp, varPop, varSamp,
    corr, covarPop, covarSamp, argMin, argMax, topK, uniq, uniqExact,
    groupArray, groupUniqArray,
    # Window functions
    rowNumber, rank, denseRank, lagInFrame, leadInFrame, firstValue, lastValue,
    # Other functions
    neighbor, runningAccumulate, runningDifference,
)
from chpy.functions.base import WindowSpec
from chpy.orm import Subquery, Table, Column
from datetime import datetime, timedelta
import sys
import argparse
from datetime import datetime, timedelta
import sys
import argparse


# ============================================================================
# Individual Example Functions
# ============================================================================

def example_1_basic_query(table):
    """Example 1: Basic query using column objects."""
    print("1. Basic query using column objects (with autocomplete)...")
    print("-" * 70)
    df = (table.query()
        .select(crypto_quotes.pair, crypto_quotes.best_bid_price, crypto_quotes.timestamp_ms)
        .where(crypto_quotes.pair == "BTC-USDT")
        .where(crypto_quotes.exchange == "BINANCE")
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        .limit(10)
        .to_dataframe())
    print(f"   DataFrame shape: {df.shape}")
    if not df.empty:
        print(f"   Columns: {list(df.columns)}")
        print(f"   Sample data:\n{df.head(3)}")
    else:
        print("   No data found")


def example_2_direct_column_access(table):
    """Example 2: Direct column access."""
    print("2. Using direct column access...")
    print("-" * 70)
    result = (table.query()
        .where(table.pair == "BTC-USDT")
        .where(table.best_bid_price > 50000)
        .where(table.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        .order_by(table.timestamp_ms, desc=True)
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results")
    if result:
        print(f"   First result: pair={result[0].get('pair')}, bid={result[0].get('best_bid_price')}")


def example_3_complex_expressions(table):
    """Example 3: Complex expressions with AND/OR."""
    print("3. Complex expressions with AND/OR operators...")
    print("-" * 70)
    result = (table.query()
        .where(
            (crypto_quotes.pair == "BTC-USDT") & 
            (crypto_quotes.exchange.in_(["BINANCE", "KUCOIN"])) &
            (crypto_quotes.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        )
        .limit(10)
        .to_list())
    print(f"   Found {len(result)} results with complex AND conditions")


def example_4_multiple_where(table):
    """Example 4: Multiple where conditions."""
    print("4. Multiple where conditions (chained)...")
    print("-" * 70)
    result = (table.query()
        .where(crypto_quotes.pair == "BTC-USDT")
        .where(crypto_quotes.exchange == "BINANCE")
        .where(crypto_quotes.best_bid_price > 50000)
        .where(crypto_quotes.best_ask_price < 60000)
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results with multiple where clauses")


def example_5_column_select(table):
    """Example 5: Selecting specific columns."""
    print("5. Selecting specific columns using column objects...")
    print("-" * 70)
    df = (table.query()
        .select(
            crypto_quotes.pair,
            crypto_quotes.best_bid_price,
            crypto_quotes.best_ask_price,
            crypto_quotes.timestamp_ms,
            crypto_quotes.exchange
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        .limit(10)
        .to_dataframe())
    print(f"   Selected columns: {list(df.columns)}")
    print(f"   Rows: {len(df)}")


def example_6_comparison_operators(table):
    """Example 6: Comparison operators."""
    print("6. Using comparison operators (>, <, >=, <=)...")
    print("-" * 70)
    result = (table.query()
        .where(crypto_quotes.best_bid_price > 50000)
        .where(crypto_quotes.best_bid_price < 60000)
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        .order_by(crypto_quotes.best_bid_price, desc=False)
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results with price range filter")


def example_7_in_operator(table):
    """Example 7: IN operator."""
    print("7. Using IN operator for multiple values...")
    print("-" * 70)
    result = (table.query()
        .where(crypto_quotes.pair.in_(["BTC-USDT", "ETH-USDT", "BNB-USDT"]))
        .where(crypto_quotes.exchange == "BINANCE")
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        .order_by(crypto_quotes.pair, desc=False)
        .limit(15)
        .to_list())
    print(f"   Found {len(result)} results for multiple pairs")


def example_8_group_by(table):
    """Example 8: Grouping and aggregation."""
    print("8. Grouping and aggregation with column objects and aggregate functions...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            crypto_quotes.exchange,
            avg(crypto_quotes.best_bid_price).alias("avg_bid"),
            count().alias("cnt")
        )
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        .group_by(crypto_quotes.pair, crypto_quotes.exchange)
        .having("avg_bid > 0")
        .order_by("avg_bid", desc=True)
        .limit(10)
        .to_list())
    print(f"   Found {len(result)} grouped results")
    if result:
        print(f"   Sample: {result[0]}")


def example_9_order_by(table):
    """Example 9: Ordering by column objects."""
    print("9. Ordering by column objects...")
    print("-" * 70)
    result = (table.query()
        .where(crypto_quotes.pair == "BTC-USDT")
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        .order_by(crypto_quotes.exchange, desc=False)
        .order_by(crypto_quotes.timestamp_ms, desc=True)
        .limit(10)
        .to_list())
    print(f"   Found {len(result)} results ordered by exchange and timestamp")


def example_10_count(table):
    """Example 10: Counting rows."""
    print("10. Counting rows with column expressions...")
    print("-" * 70)
    count = (table.query()
        .where(crypto_quotes.pair == "BTC-USDT")
        .where(crypto_quotes.exchange == "BINANCE")
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        .count())
    print(f"   Count: {count} rows")


def example_11_first(table):
    """Example 11: Getting first result."""
    print("11. Getting first result...")
    print("-" * 70)
    first = (table.query()
        .where(crypto_quotes.pair == "BTC-USDT")
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        .order_by(crypto_quotes.timestamp_ms, desc=True)
        .first())
    if first:
        print(f"   First quote: pair={first.get('pair')}, bid={first.get('best_bid_price')}, "
              f"ask={first.get('best_ask_price')}")
    else:
        print("   No results found")


def example_12_exists(table):
    """Example 12: Checking existence."""
    print("12. Checking if results exist...")
    print("-" * 70)
    exists = (table.query()
        .where(crypto_quotes.pair == "BTC-USDT")
        .where(crypto_quotes.exchange == "BINANCE")
        .exists())
    print(f"   Exists: {exists}")


def example_13_export_formats(table):
    """Example 13: Exporting to different formats."""
    print("13. Exporting to different formats...")
    print("-" * 70)
    json_data = (table.query()
        .where(crypto_quotes.pair == "BTC-USDT")
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        .limit(3)
        .to_json(indent=2))
    print(f"   JSON length: {len(json_data)} characters")
    print(f"   First 150 chars: {json_data[:150]}...")


def example_14_dict_output(table):
    """Example 14: Dictionary output."""
    print("14. Getting results as dictionary...")
    print("-" * 70)
    pair_dict = (table.query()
        .select(crypto_quotes.pair, crypto_quotes.best_bid_price)
        .where(crypto_quotes.pair == "BTC-USDT")
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        .limit(3)
        .to_dict(crypto_quotes.pair, crypto_quotes.best_bid_price))
    print(f"   Dictionary: {pair_dict}")


def example_15_iterate(table):
    """Example 15: Iterating over results."""
    print("15. Iterating over results...")
    print("-" * 70)
    count = 0
    for quote in table.query().where(crypto_quotes.pair == "BTC-USDT").limit(3):
        count += 1
        print(f"   Quote {count}: pair={quote.get('pair')}, bid={quote.get('best_bid_price')}")


def example_16_not_in(table):
    """Example 16: NOT IN operator."""
    print("16. Using NOT IN operator...")
    print("-" * 70)
    result = (table.query()
        .where(crypto_quotes.exchange.not_in(["BINANCE", "KUCOIN"]))
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results from exchanges other than BINANCE/KUCOIN")


def example_17_like(table):
    """Example 17: LIKE operator."""
    print("17. Using LIKE operator...")
    print("-" * 70)
    result = (table.query()
        .where(crypto_quotes.pair.like("BTC-%"))
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results with pairs starting with 'BTC-'")


def example_18_or_expression(table):
    """Example 18: Complex OR expression."""
    print("18. Complex OR expression...")
    print("-" * 70)
    result = (table.query()
        .where(
            (crypto_quotes.pair == "BTC-USDT") | 
            (crypto_quotes.pair == "ETH-USDT")
        )
        .where(crypto_quotes.exchange == "BINANCE")
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        .limit(10)
        .to_list())
    print(f"   Found {len(result)} results for BTC-USDT OR ETH-USDT")


def example_19_direct_column_access(table):
    """Example 19: Direct column access from table instance."""
    print("19. Using direct column access from table instance...")
    print("-" * 70)
    result = (table.query()
        .where(table.pair == "BTC-USDT")
        .where(table.best_bid_price > 50000)
        .where(table.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        .limit(3)
        .to_list())
    print(f"   Found {len(result)} results using direct column access")


def example_20_time_range(table):
    """Example 20: Time range queries."""
    print("20. Time range queries with datetime objects...")
    print("-" * 70)
    end_time = datetime.now()
    start_time = datetime(2025, 12, 20, 0, 0, 0)
    result = (table.query()
        .where(crypto_quotes.pair == "BTC-USDT")
        .where(crypto_quotes.timestamp_ms >= start_time)
        .where(crypto_quotes.timestamp_ms <= end_time)
        .order_by(crypto_quotes.timestamp_ms, desc=True)
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results in the last 24 hours")


def example_21_multiple_aggregations(table):
    """Example 21: Multiple aggregations."""
    print("21. Multiple aggregations in select using aggregate functions...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            min(crypto_quotes.best_bid_price).alias("min_bid"),
            max(crypto_quotes.best_bid_price).alias("max_bid"),
            avg(crypto_quotes.best_bid_price).alias("avg_bid"),
            count().alias("cnt")
        )
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 20, 0, 0, 0))
        .group_by(crypto_quotes.pair)
        .having("cnt > 10")
        .order_by("avg_bid", desc=True)
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} aggregated results")
    if result:
        print(f"   Sample: {result[0]}")


def example_22_helpers(table):
    """Example 22: Using helper methods."""
    print("22. Using exchange and pair helper methods...")
    print("-" * 70)
    exchanges = table.get_valid_exchanges()
    print(f"   Valid exchanges: {exchanges}")
    
    if exchanges:
        binance_pairs = table.get_exchange_pairs("BINANCE")
        print(f"   Binance pairs (first 5): {binance_pairs[:5]}")
        
        is_valid = table.is_valid_pair("BTC-USDT", "BINANCE")
        print(f"   Is BTC-USDT valid for BINANCE: {is_valid}")


def example_23_numpy(table):
    """Example 23: NumPy array output."""
    print("23. Getting results as NumPy array...")
    print("-" * 70)
    try:
        arr = (table.query()
            .select(crypto_quotes.best_bid_price, crypto_quotes.best_ask_price, crypto_quotes.timestamp_ms)
            .where(crypto_quotes.pair == "BTC-USDT")
            .limit(10)
            .to_numpy())
        print(f"   Array shape: {arr.shape}")
        print(f"   Array dtype: {arr.dtype}")
    except Exception as e:
        print(f"   Error: {e}")


def example_24_csv(table):
    """Example 24: CSV export."""
    print("24. Exporting to CSV string...")
    print("-" * 70)
    csv_data = (table.query()
        .select(crypto_quotes.pair, crypto_quotes.best_bid_price, crypto_quotes.best_ask_price)
        .where(crypto_quotes.pair == "BTC-USDT")
        .limit(5)
        .to_csv())
    print(f"   CSV length: {len(csv_data)} characters")
    print(f"   First 200 chars:\n{csv_data[:200]}")


def example_25_inequality(table):
    """Example 25: Inequality operators."""
    print("25. Using inequality operators (!=, <, <=, >, >=)...")
    print("-" * 70)
    result = (table.query()
        .where(crypto_quotes.pair != "ETH-USDT")
        .where(crypto_quotes.best_bid_price >= 1000)
        .where(crypto_quotes.best_bid_price <= 100000)
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results with inequality filters")


def example_26_string_functions(table):
    """Example 26: String functions."""
    print("26. Using string functions (length, upper, lower, substring)...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            length(crypto_quotes.pair).alias("pair_length"),
            upper(crypto_quotes.pair).alias("pair_upper"),
            lower(crypto_quotes.exchange).alias("exchange_lower"),
            substring(crypto_quotes.pair, 1, 3).alias("pair_prefix")
        )
        .where(crypto_quotes.pair.in_(["BTC-USDT", "ETH-USDT"]))
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results with string function transformations")
    if result:
        print(f"   Sample: {result[0]}")


def example_27_date_time_functions(table):
    """Example 27: Date and time functions."""
    print("27. Using date/time functions (toYear, toMonth, toHour)...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.timestamp_ms,
            toYear(toDateTime(divide(crypto_quotes.timestamp_ms, 1000))).alias("year"),
            toMonth(toDateTime(divide(crypto_quotes.timestamp_ms, 1000))).alias("month"),
            toDayOfMonth(toDateTime(divide(crypto_quotes.timestamp_ms, 1000))).alias("day"),
            toHour(toDateTime(divide(crypto_quotes.timestamp_ms, 1000))).alias("hour")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results with date/time extractions")
    if result:
        print(f"   Sample: {result[0]}")


def example_28_math_functions(table):
    """Example 28: Mathematical functions."""
    print("28. Using math functions (abs, sqrt, round, floor, ceil)...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.best_bid_price,
            crypto_quotes.best_ask_price,
            abs(crypto_quotes.best_bid_price).alias("abs_bid"),
            sqrt(crypto_quotes.best_bid_price).alias("sqrt_bid"),
            round(crypto_quotes.best_bid_price).alias("rounded_bid"),
            floor(crypto_quotes.best_bid_price).alias("floor_bid"),
            ceil(crypto_quotes.best_ask_price).alias("ceil_ask")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .where(crypto_quotes.best_bid_price > 0)
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results with math function transformations")
    if result:
        print(f"   Sample: {result[0]}")


def example_29_conditional_functions(table):
    """Example 29: Conditional functions."""
    print("29. Using conditional functions (if, coalesce)...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            crypto_quotes.best_bid_price,
            crypto_quotes.best_ask_price,
            if_func(
                crypto_quotes.best_bid_price > 50000,
                "high",
                "normal"
            ).alias("price_category")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results with conditional logic")
    if result:
        print(f"   Sample: {result[0]}")


def example_30_type_conversion(table):
    """Example 30: Type conversion functions."""
    print("30. Using type conversion functions (toString, toInt64, toFloat64)...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            toString(crypto_quotes.best_bid_price).alias("bid_as_string"),
            toInt64(crypto_quotes.best_bid_price).alias("bid_as_int"),
            toFloat64(crypto_quotes.best_bid_price).alias("bid_as_float")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .limit(3)
        .to_list())
    print(f"   Found {len(result)} results with type conversions")
    if result:
        print(f"   Sample: {result[0]}")


def example_31_string_pattern_matching(table):
    """Example 31: String pattern matching functions."""
    print("31. Using string pattern matching (startsWith, endsWith)...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            startsWith(crypto_quotes.pair, "BTC").alias("starts_with_btc"),
            endsWith(crypto_quotes.pair, "USDT").alias("ends_with_usdt")
        )
        .where(crypto_quotes.pair.in_(["BTC-USDT", "ETH-USDT", "BNB-USDT"]))
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results with pattern matching")
    if result:
        print(f"   Sample: {result[0]}")


def example_32_combined_functions(table):
    """Example 32: Combining multiple functions."""
    print("32. Combining multiple functions in a single query...")
    print("-" * 70)
    result = (table.query()
        .select(
            upper(crypto_quotes.pair).alias("pair_upper"),
            length(crypto_quotes.pair).alias("pair_length"),
            round(crypto_quotes.best_bid_price).alias("rounded_price"),
            toYear(toDateTime(divide(crypto_quotes.timestamp_ms, 1000))).alias("year"),
            toMonth(toDateTime(divide(crypto_quotes.timestamp_ms, 1000))).alias("month"),
            if_func(
                crypto_quotes.best_bid_price > 50000,
                "premium",
                "standard"
            ).alias("tier")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .limit(3)
        .to_list())
    print(f"   Found {len(result)} results with combined functions")
    if result:
        print(f"   Sample: {result[0]}")


def example_33_window_functions_basic(table):
    """Example 33: Basic window functions with PARTITION BY."""
    print("33. Basic window functions with PARTITION BY...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            crypto_quotes.exchange,
            crypto_quotes.best_bid_price,
            crypto_quotes.timestamp_ms,
            avg(crypto_quotes.best_bid_price).over(
                WindowSpec().partition_by(crypto_quotes.pair)
            ).alias("avg_price_by_pair"),
            rowNumber().over(
                WindowSpec()
                .partition_by(crypto_quotes.pair, crypto_quotes.exchange)
                .order_by(crypto_quotes.timestamp_ms, desc=True)
            ).alias("row_num")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 22, 0, 0, 0))
        .limit(10)
        .to_list())
    print(f"   Found {len(result)} results with window functions")
    if result:
        print(f"   Sample: pair={result[0].get('pair')}, avg_price={result[0].get('avg_price_by_pair')}, row_num={result[0].get('row_num')}")


def example_34_window_rank_functions(table):
    """Example 34: Ranking window functions."""
    print("34. Using ranking window functions (rank, denseRank)...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            crypto_quotes.exchange,
            crypto_quotes.best_bid_price,
            rank().over(
                WindowSpec()
                .partition_by(crypto_quotes.pair)
                .order_by(crypto_quotes.best_bid_price, desc=True)
            ).alias("price_rank"),
            denseRank().over(
                WindowSpec()
                .partition_by(crypto_quotes.pair)
                .order_by(crypto_quotes.best_bid_price, desc=True)
            ).alias("price_dense_rank")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .limit(10)
        .to_list())
    print(f"   Found {len(result)} results with ranking functions")
    if result:
        print(f"   Sample: price={result[0].get('best_bid_price')}, rank={result[0].get('price_rank')}")


def example_35_window_lag_lead(table):
    """Example 35: LAG and LEAD window functions."""
    print("35. Using LAG and LEAD window functions...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            crypto_quotes.timestamp_ms,
            crypto_quotes.best_bid_price,
            lagInFrame(crypto_quotes.best_bid_price, 1).over(
                WindowSpec()
                .partition_by(crypto_quotes.pair)
                .order_by(crypto_quotes.timestamp_ms, desc=False)
            ).alias("prev_price"),
            leadInFrame(crypto_quotes.best_bid_price, 1).over(
                WindowSpec()
                .partition_by(crypto_quotes.pair)
                .order_by(crypto_quotes.timestamp_ms, desc=False)
            ).alias("next_price")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .limit(10)
        .to_list())
    print(f"   Found {len(result)} results with LAG/LEAD functions")
    if result:
        sample = result[0]
        print(f"   Sample: price={sample.get('best_bid_price')}, prev={sample.get('prev_price')}, next={sample.get('next_price')}")


def example_36_window_rows_between(table):
    """Example 36: Window functions with ROWS BETWEEN frame."""
    print("36. Window functions with ROWS BETWEEN frame...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            crypto_quotes.timestamp_ms,
            crypto_quotes.best_bid_price,
            avg(crypto_quotes.best_bid_price).over(
                WindowSpec()
                .partition_by(crypto_quotes.pair)
                .order_by(crypto_quotes.timestamp_ms, desc=False)
                .rows_between("UNBOUNDED PRECEDING", "CURRENT ROW")
            ).alias("running_avg")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .limit(10)
        .to_list())
    print(f"   Found {len(result)} results with running average")
    if result:
        print(f"   Sample: price={result[0].get('best_bid_price')}, running_avg={result[0].get('running_avg')}")


def example_37_advanced_aggregates(table):
    """Example 37: Advanced aggregate functions (quantile, stddev, corr)."""
    print("37. Advanced aggregate functions (quantile, stddev, correlation)...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            avg(crypto_quotes.best_bid_price).alias("avg_bid"),
            quantile(0.5)(crypto_quotes.best_bid_price).alias("median_bid"),
            quantile(0.95)(crypto_quotes.best_bid_price).alias("p95_bid"),
            stddevPop(crypto_quotes.best_bid_price).alias("stddev_bid"),
            min(crypto_quotes.best_bid_price).alias("min_bid"),
            max(crypto_quotes.best_bid_price).alias("max_bid")
        )
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 22, 0, 0, 0))
        .group_by(crypto_quotes.pair)
        .having("count() > 10")
        .order_by("avg_bid", desc=True)
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} aggregated results")
    if result:
        print(f"   Sample: {result[0]}")


def example_38_correlation_analysis(table):
    """Example 38: Correlation analysis between bid and ask prices."""
    print("38. Correlation analysis between bid and ask prices...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            avg(crypto_quotes.best_bid_price).alias("avg_bid"),
            avg(crypto_quotes.best_ask_price).alias("avg_ask"),
            corr(crypto_quotes.best_bid_price, crypto_quotes.best_ask_price).alias("bid_ask_corr"),
            covarPop(crypto_quotes.best_bid_price, crypto_quotes.best_ask_price).alias("bid_ask_covar")
        )
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 22, 0, 0, 0))
        .group_by(crypto_quotes.pair)
        .having("count() > 50")
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} correlation results")
    if result:
        print(f"   Sample: {result[0]}")


def example_39_argmin_argmax(table):
    """Example 39: argMin and argMax functions."""
    print("39. Using argMin and argMax to find extrema...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            min(crypto_quotes.best_bid_price).alias("min_price"),
            argMin(crypto_quotes.timestamp_ms, crypto_quotes.best_bid_price).alias("min_price_time"),
            max(crypto_quotes.best_bid_price).alias("max_price"),
            argMax(crypto_quotes.timestamp_ms, crypto_quotes.best_bid_price).alias("max_price_time")
        )
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 22, 0, 0, 0))
        .group_by(crypto_quotes.pair)
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results with argMin/argMax")
    if result:
        print(f"   Sample: {result[0]}")


def example_40_topk_groupby(table):
    """Example 40: topK aggregate function."""
    print("40. Using topK to get most common exchanges per pair...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            topK(3)(crypto_quotes.exchange).alias("top_exchanges")
        )
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 22, 0, 0, 0))
        .group_by(crypto_quotes.pair)
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results with topK")
    if result:
        print(f"   Sample: {result[0]}")


def example_41_unique_counts(table):
    """Example 41: Unique count functions (uniq, uniqExact)."""
    print("41. Using unique count functions...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            count().alias("total_count"),
            uniq(crypto_quotes.exchange).alias("unique_exchanges"),
            uniqExact(crypto_quotes.exchange).alias("unique_exchanges_exact")
        )
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 22, 0, 0, 0))
        .group_by(crypto_quotes.pair)
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results with unique counts")
    if result:
        print(f"   Sample: {result[0]}")


def example_42_group_array(table):
    """Example 42: Grouping into arrays."""
    print("42. Grouping values into arrays...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            groupArray(crypto_quotes.exchange).alias("all_exchanges"),
            groupArray(crypto_quotes.best_bid_price).alias("all_prices"),
            groupUniqArray(crypto_quotes.exchange).alias("unique_exchanges")
        )
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 22, 0, 0, 0))
        .group_by(crypto_quotes.pair)
        .limit(3)
        .to_list())
    print(f"   Found {len(result)} results with groupArray")
    if result:
        sample = result[0]
        exchanges = sample.get('all_exchanges', [])
        print(f"   Sample: pair={sample.get('pair')}, exchange_count={len(exchanges) if exchanges else 0}")


def example_43_string_replace_functions(table):
    """Example 43: String replacement and manipulation."""
    print("43. String replacement and manipulation functions...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            replace(crypto_quotes.pair, "-", "_").alias("pair_underscore"),
            replaceAll(crypto_quotes.pair, "USDT", "USD").alias("pair_usd"),
            splitByChar("-", crypto_quotes.pair).alias("pair_parts"),
            reverse(crypto_quotes.pair).alias("pair_reversed"),
            trimBoth(crypto_quotes.pair).alias("pair_trimmed")
        )
        .where(crypto_quotes.pair.in_(["BTC-USDT", "ETH-USDT"]))
        .limit(3)
        .to_list())
    print(f"   Found {len(result)} results with string functions")
    if result:
        print(f"   Sample: {result[0]}")


def example_44_string_extract_functions(table):
    """Example 44: String extraction functions."""
    print("44. String extraction functions...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            left(crypto_quotes.pair, 3).alias("left_3"),
            right(crypto_quotes.pair, 4).alias("right_4"),
            position(crypto_quotes.pair, "-").alias("dash_position"),
            extractAll(crypto_quotes.pair, "[A-Z]+").alias("extracted_letters")
        )
        .where(crypto_quotes.pair.in_(["BTC-USDT", "ETH-USDT"]))
        .limit(3)
        .to_list())
    print(f"   Found {len(result)} results with extraction functions")
    if result:
        print(f"   Sample: {result[0]}")


def example_45_date_time_advanced(table):
    """Example 45: Advanced date/time functions."""
    print("45. Advanced date/time functions...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.timestamp_ms,
            toStartOfDay(toDateTime(divide(crypto_quotes.timestamp_ms, 1000))).alias("start_of_day"),
            toStartOfHour(toDateTime(divide(crypto_quotes.timestamp_ms, 1000))).alias("start_of_hour"),
            toStartOfMonth(toDateTime(divide(crypto_quotes.timestamp_ms, 1000))).alias("start_of_month"),
            toStartOfYear(toDateTime(divide(crypto_quotes.timestamp_ms, 1000))).alias("start_of_year"),
            toQuarter(toDateTime(divide(crypto_quotes.timestamp_ms, 1000))).alias("quarter"),
            toDayOfWeek(toDateTime(divide(crypto_quotes.timestamp_ms, 1000))).alias("day_of_week")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results with advanced date/time functions")
    if result:
        print(f"   Sample: {result[0]}")


def example_46_date_arithmetic(table):
    """Example 46: Date arithmetic functions."""
    print("46. Date arithmetic functions...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.timestamp_ms,
            toDateTime(divide(crypto_quotes.timestamp_ms, 1000)).alias("current_time"),
            addHours(toDateTime(divide(crypto_quotes.timestamp_ms, 1000)), 1).alias("plus_one_hour"),
            subtractHours(toDateTime(divide(crypto_quotes.timestamp_ms, 1000)), 2).alias("minus_two_hours"),
            addMinutes(toDateTime(divide(crypto_quotes.timestamp_ms, 1000)), 30).alias("plus_thirty_min"),
            dateDiff(
                "hour",
                toDateTime(divide(crypto_quotes.timestamp_ms, 1000)),
                now()
            ).alias("hours_since_quote")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .limit(3)
        .to_list())
    print(f"   Found {len(result)} results with date arithmetic")
    if result:
        print(f"   Sample: {result[0]}")


def example_47_math_advanced(table):
    """Example 47: Advanced mathematical functions."""
    print("47. Advanced mathematical functions...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.best_bid_price,
            log(crypto_quotes.best_bid_price).alias("log_price"),
            log10(crypto_quotes.best_bid_price).alias("log10_price"),
            exp(divide(crypto_quotes.best_bid_price, 100000)).alias("exp_scaled"),
            pow(crypto_quotes.best_bid_price, 0.5).alias("sqrt_equivalent"),
            power(crypto_quotes.best_bid_price, 2).alias("price_squared")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .where(crypto_quotes.best_bid_price > 0)
        .limit(3)
        .to_list())
    print(f"   Found {len(result)} results with advanced math functions")
    if result:
        print(f"   Sample: {result[0]}")


def example_48_trigonometric_functions(table):
    """Example 48: Trigonometric functions."""
    print("48. Trigonometric functions...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.best_bid_price,
            sin(divide(crypto_quotes.best_bid_price, 100000)).alias("sin_scaled"),
            cos(divide(crypto_quotes.best_bid_price, 100000)).alias("cos_scaled"),
            tan(divide(crypto_quotes.best_bid_price, 100000)).alias("tan_scaled"),
            asin(divide(crypto_quotes.best_bid_price, 1000000)).alias("arcsin_scaled"),
            atan(divide(crypto_quotes.best_bid_price, 100000)).alias("arctan_scaled")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .where(crypto_quotes.best_bid_price > 0)
        .limit(3)
        .to_list())
    print(f"   Found {len(result)} results with trigonometric functions")
    if result:
        print(f"   Sample: {result[0]}")


def example_49_conditional_multiif(table):
    """Example 49: Multi-conditional function (multiIf)."""
    print("49. Using multiIf for multiple conditions...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            crypto_quotes.best_bid_price,
            multiIf(
                crypto_quotes.best_bid_price > 100000, "very_high",
                crypto_quotes.best_bid_price > 50000, "high",
                crypto_quotes.best_bid_price > 10000, "medium",
                "low"
            ).alias("price_category")
        )
        .where(crypto_quotes.pair.in_(["BTC-USDT", "ETH-USDT", "BNB-USDT"]))
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results with multiIf")
    if result:
        print(f"   Sample: {result[0]}")


def example_50_null_handling(table):
    """Example 50: Null handling functions."""
    print("50. Null handling functions (ifNull, coalesce, nullIf)...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            crypto_quotes.best_bid_price,
            crypto_quotes.best_ask_price,
            ifNull(crypto_quotes.best_bid_price, 0).alias("bid_with_default"),
            coalesce(
                crypto_quotes.best_bid_price,
                crypto_quotes.best_ask_price,
                0
            ).alias("first_non_null_price"),
            nullIf(crypto_quotes.best_bid_price, crypto_quotes.best_ask_price).alias("bid_if_not_equal_ask")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .limit(3)
        .to_list())
    print(f"   Found {len(result)} results with null handling")
    if result:
        print(f"   Sample: {result[0]}")


def example_51_array_basic_operations(table):
    """Example 51: Basic array operations."""
    print("51. Basic array operations...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            crypto_quotes.bid_prices,
            arrayElement(crypto_quotes.bid_prices, 1).alias("first_bid"),
            arraySum(crypto_quotes.bid_prices).alias("total_bid_amount"),
            arrayAvg(crypto_quotes.bid_prices).alias("avg_bid_price"),
            arrayMax(crypto_quotes.bid_prices).alias("max_bid_price"),
            arrayMin(crypto_quotes.bid_prices).alias("min_bid_price")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .where("length(bid_prices) > 0")
        .limit(3)
        .to_list())
    print(f"   Found {len(result)} results with array operations")
    if result:
        sample = result[0]
        bid_prices = sample.get('bid_prices', [])
        print(f"   Sample: pair={sample.get('pair')}, array_length={len(bid_prices) if bid_prices else 0}")


def example_52_array_manipulation(table):
    """Example 52: Array manipulation functions."""
    print("52. Array manipulation functions...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            crypto_quotes.bid_prices,
            arraySlice(crypto_quotes.bid_prices, 1, 3).alias("first_3_bids"),
            arraySort(crypto_quotes.bid_prices).alias("sorted_bids"),
            arrayReverse(crypto_quotes.bid_prices).alias("reversed_bids"),
            arrayDistinct(crypto_quotes.bid_prices).alias("unique_bids"),
            has(crypto_quotes.bid_prices, 50000).alias("has_50000")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .where("length(bid_prices) > 0")
        .limit(3)
        .to_list())
    print(f"   Found {len(result)} results with array manipulation")
    if result:
        sample = result[0]
        print(f"   Sample: pair={sample.get('pair')}, has_50000={sample.get('has_50000')}")


def example_53_array_filter_map(table):
    """Example 53: Array filtering and mapping."""
    print("53. Array filtering and mapping functions...")
    print("-" * 70)
    # Note: arrayFilter and arrayMap require lambda expressions in ClickHouse
    # This example shows how they might be used, but actual implementation may vary
    result = (table.query()
        .select(
            crypto_quotes.pair,
            crypto_quotes.bid_prices,
            length(crypto_quotes.bid_prices).alias("bid_count"),
            arraySum(crypto_quotes.bid_prices).alias("total_bids")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .where("length(bid_prices) > 0")
        .limit(3)
        .to_list())
    print(f"   Found {len(result)} results")
    if result:
        print(f"   Sample: {result[0]}")


def example_54_subquery_exists(table):
    """Example 54: EXISTS subquery."""
    print("54. Using EXISTS subquery...")
    print("-" * 70)
    # Note: EXISTS subqueries may not work in distributed ClickHouse setups
    # This example demonstrates the syntax but uses a direct filter instead
    # for compatibility with distributed environments
    print("   EXISTS subquery syntax (may not work in distributed setups):")
    print("   ```")
    print("   subq_builder = (table.query()")
    print("       .where(crypto_quotes.exchange == 'BINANCE'))")
    print("   result = (table.query()")
    print("       .where(Subquery.exists(subq_builder))")
    print("       .to_list())")
    print("   ```")
    print("   ")
    print("   Using direct filter instead for distributed compatibility:")
    
    # Use direct filter instead of EXISTS to avoid distributed query issues
    result = (table.query()
        .select(crypto_quotes.pair, crypto_quotes.exchange, crypto_quotes.best_bid_price)
        .where(crypto_quotes.exchange == "BINANCE")
        .where(crypto_quotes.pair == "BTC-USDT")
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results (equivalent to EXISTS subquery)")
    if result:
        print(f"   Sample: {result[0]}")


def example_55_subquery_in(table):
    """Example 55: IN subquery."""
    print("55. Using IN subquery...")
    print("-" * 70)
    # Note: IN subqueries may not work in distributed ClickHouse setups
    # This example demonstrates the syntax but uses a direct filter instead
    # for compatibility with distributed environments
    print("   IN subquery syntax (may not work in distributed setups):")
    print("   ```")
    print("   subq_builder = (table.query()")
    print("       .select(crypto_quotes.pair)")
    print("       .where(crypto_quotes.exchange == 'BINANCE')")
    print("       .group_by(crypto_quotes.pair))")
    print("   result = (table.query()")
    print("       .where(crypto_quotes.pair.in_(Subquery(subq_builder)))")
    print("       .to_list())")
    print("   ```")
    print("   ")
    print("   Using direct filter instead for distributed compatibility:")
    
    # Use direct filter instead of IN subquery to avoid distributed query issues
    result = (table.query()
        .select(crypto_quotes.pair, crypto_quotes.exchange, avg(crypto_quotes.best_bid_price).alias("avg_bid"))
        .where(crypto_quotes.pair.in_(["BTC-USDT", "ETH-USDT", "BNB-USDT"]))
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 22, 0, 0, 0))
        .group_by(crypto_quotes.pair, crypto_quotes.exchange)
        .limit(10)
        .to_list())
    print(f"   Found {len(result)} results (equivalent to IN subquery)")
    if result:
        print(f"   Sample: {result[0]}")


def example_56_subquery_scalar(table):
    """Example 56: Scalar subquery in SELECT."""
    print("56. Using scalar subquery in SELECT clause...")
    print("-" * 70)
    # Compare each quote's price to the overall average
    avg_price_subq = (table.query()
        .select(avg(crypto_quotes.best_bid_price))
        .where(crypto_quotes.pair == "BTC-USDT")
        .where(crypto_quotes.timestamp_ms >= datetime.now() - timedelta(days=1)))
    
    result = (table.query()
        .select(
            crypto_quotes.pair,
            crypto_quotes.best_bid_price,
            crypto_quotes.timestamp_ms,
            Subquery(avg_price_subq).alias("overall_avg_price")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results with scalar subquery")
    if result:
        print(f"   Sample: {result[0]}")


def example_57_subquery_from(table):
    """Example 57: Subquery in FROM clause (derived table)."""
    print("57. Using subquery in FROM clause (derived table)...")
    print("-" * 70)
    # First create a subquery that aggregates by pair and exchange
    subq_builder = (table.query()
        .select(
            crypto_quotes.pair,
            crypto_quotes.exchange,
            avg(crypto_quotes.best_bid_price).alias("avg_bid"),
            count().alias("quote_count")
        )
        .where(crypto_quotes.timestamp_ms >= datetime.now() - timedelta(days=1))
        .group_by(crypto_quotes.pair, crypto_quotes.exchange))
    
    # Then query from that derived table
    # Note: We need to use raw SQL for columns from derived table since schema won't match
    subq = Subquery(subq_builder)
    result = (table.query()
        .from_subquery(subq, alias="daily_avg")
        .select("pair", "exchange", "avg_bid", "quote_count")
        .where("avg_bid > 0")
        .order_by("quote_count", desc=True)
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results from derived table")
    if result:
        print(f"   Sample: {result[0]}")


def example_58_join_inner(table):
    """Example 58: INNER JOIN (conceptual - requires another table)."""
    print("58. INNER JOIN example (note: requires another table)...")
    print("-" * 70)
    print("   This example demonstrates JOIN syntax, but requires another table.")
    print("   Example structure:")
    print("   ```")
    print("   # Create another table schema")
    print("   other_columns = [Column('symbol', 'String'), Column('name', 'String')]")
    print("   other_table = Table('market_data', 'stockhouse', other_columns)")
    print("   ")
    print("   result = (table.query()")
    print("       .select(crypto_quotes.pair, other_table.name)")
    print("       .join(other_table, condition=(crypto_quotes.pair == other_table.symbol))")
    print("       .to_list())")
    print("   ```")
    print("   Skipping actual execution (requires second table)")


def example_59_having_with_expressions(table):
    """Example 59: HAVING clause with expressions."""
    print("59. HAVING clause with complex expressions...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            avg(crypto_quotes.best_bid_price).alias("avg_bid"),
            max(crypto_quotes.best_bid_price).alias("max_bid"),
            min(crypto_quotes.best_bid_price).alias("min_bid"),
            count().alias("cnt")
        )
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 22, 0, 0, 0))
        .group_by(crypto_quotes.pair)
        .having("avg_bid > 1000 AND cnt > 10 AND (max_bid - min_bid) > 100")
        .order_by("avg_bid", desc=True)
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results with HAVING expressions")
    if result:
        print(f"   Sample: {result[0]}")


def example_60_parquet_export(table):
    """Example 60: Exporting to Parquet format."""
    print("60. Exporting to Parquet format...")
    print("-" * 70)
    try:
        import tempfile
        import os
        with tempfile.NamedTemporaryFile(delete=False, suffix='.parquet') as tmp:
            tmp_path = tmp.name
        
        (table.query()
            .select(
                crypto_quotes.pair,
                crypto_quotes.exchange,
                crypto_quotes.best_bid_price,
                crypto_quotes.best_ask_price,
                crypto_quotes.timestamp_ms
            )
            .where(crypto_quotes.pair == "BTC-USDT")
            .limit(10)
            .to_parquet(tmp_path))
        
        file_size = os.path.getsize(tmp_path)
        print(f"   Exported to Parquet file: {tmp_path}")
        print(f"   File size: {file_size} bytes")
        os.unlink(tmp_path)
        print("   Temporary file cleaned up")
    except Exception as e:
        print(f"   Error: {e}")


def example_61_running_functions(table):
    """Example 61: Running accumulation functions (using window functions)."""
    print("61. Running accumulation functions (using window functions)...")
    print("-" * 70)
    # Note: runningAccumulate and runningDifference are deprecated
    # Use window functions instead (sum().over() with ROWS BETWEEN for running sum)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            crypto_quotes.timestamp_ms,
            crypto_quotes.best_bid_price,
            sum(crypto_quotes.best_bid_price).over(
                WindowSpec()
                .partition_by(crypto_quotes.pair)
                .order_by(crypto_quotes.timestamp_ms, desc=False)
                .rows_between("UNBOUNDED PRECEDING", "CURRENT ROW")
            ).alias("running_sum"),
            minus(
                crypto_quotes.best_bid_price,
                lagInFrame(crypto_quotes.best_bid_price, 1, 0).over(
                    WindowSpec()
                    .partition_by(crypto_quotes.pair)
                    .order_by(crypto_quotes.timestamp_ms, desc=False)
                )
            ).alias("price_diff")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .order_by(crypto_quotes.timestamp_ms, desc=False)
        .limit(10)
        .to_list())
    print(f"   Found {len(result)} results with running functions")
    if result:
        print(f"   Sample: {result[0]}")


def example_62_neighbor_function(table):
    """Example 62: Neighbor function for accessing adjacent rows (using window functions)."""
    print("62. Using window functions to access adjacent rows (replacing deprecated neighbor)...")
    print("-" * 70)
    # Note: neighbor function is deprecated, use lagInFrame/leadInFrame window functions instead
    result = (table.query()
        .select(
            crypto_quotes.pair,
            crypto_quotes.timestamp_ms,
            crypto_quotes.best_bid_price,
            leadInFrame(crypto_quotes.best_bid_price, 1).over(
                WindowSpec()
                .partition_by(crypto_quotes.pair)
                .order_by(crypto_quotes.timestamp_ms, desc=False)
            ).alias("next_price"),
            lagInFrame(crypto_quotes.best_bid_price, 1).over(
                WindowSpec()
                .partition_by(crypto_quotes.pair)
                .order_by(crypto_quotes.timestamp_ms, desc=False)
            ).alias("prev_price")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .order_by(crypto_quotes.timestamp_ms, desc=False)
        .limit(10)
        .to_list())
    print(f"   Found {len(result)} results with window functions (lagInFrame/leadInFrame)")
    if result:
        print(f"   Sample: {result[0]}")


def example_63_price_spread_analysis(table):
    """Example 63: Bid-ask spread analysis."""
    print("63. Bid-ask spread analysis...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            crypto_quotes.exchange,
            avg(crypto_quotes.best_bid_price).alias("avg_bid"),
            avg(crypto_quotes.best_ask_price).alias("avg_ask"),
            minus(avg(crypto_quotes.best_ask_price), avg(crypto_quotes.best_bid_price)).alias("avg_spread"),
            multiply(
                divide(
                    minus(avg(crypto_quotes.best_ask_price), avg(crypto_quotes.best_bid_price)),
                    avg(crypto_quotes.best_bid_price)
                ),
                100
            ).alias("spread_percentage")
        )
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 22, 0, 0, 0))
        .group_by(crypto_quotes.pair, crypto_quotes.exchange)
        .having("count() > 10")
        .order_by("spread_percentage", desc=True)
        .limit(5)
        .to_list())
    print(f"   Found {len(result)} results with spread analysis")
    if result:
        print(f"   Sample: {result[0]}")


def example_64_time_bucketing(table):
    """Example 64: Time bucketing/aggregation by time periods."""
    print("64. Time bucketing - aggregating by time periods...")
    print("-" * 70)
    result = (table.query()
        .select(
            toStartOfHour(toDateTime(divide(crypto_quotes.timestamp_ms, 1000))).alias("hour"),
            crypto_quotes.pair,
            avg(crypto_quotes.best_bid_price).alias("avg_bid"),
            min(crypto_quotes.best_bid_price).alias("min_bid"),
            max(crypto_quotes.best_bid_price).alias("max_bid"),
            count().alias("quote_count")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .where(crypto_quotes.timestamp_ms >= datetime(2025, 12, 22, 0, 0, 0))
        .group_by("hour", crypto_quotes.pair)
        .order_by("hour", desc=True)
        .limit(10)
        .to_list())
    print(f"   Found {len(result)} results with time bucketing")
    if result:
        print(f"   Sample: {result[0]}")


def example_65_format_functions(table):
    """Example 65: Format and encoding functions."""
    print("65. Format and encoding functions...")
    print("-" * 70)
    result = (table.query()
        .select(
            crypto_quotes.pair,
            round(crypto_quotes.best_bid_price).alias("rounded_price"),
            formatReadableQuantity(crypto_quotes.best_bid_price).alias("readable_price"),
            base64Encode(toString(crypto_quotes.pair)).alias("pair_base64"),
            base64Decode(base64Encode(toString(crypto_quotes.pair))).alias("pair_decoded")
        )
        .where(crypto_quotes.pair == "BTC-USDT")
        .limit(3)
        .to_list())
    print(f"   Found {len(result)} results with format functions")
    if result:
        print(f"   Sample: {result[0]}")


# ============================================================================
# Example Registry
# ============================================================================

EXAMPLES = {
    1: ("Basic query using column objects", example_1_basic_query),
    2: ("Direct column access from table instance", example_2_direct_column_access),
    3: ("Complex expressions with AND/OR operators", example_3_complex_expressions),
    4: ("Multiple where conditions (chained)", example_4_multiple_where),
    5: ("Selecting specific columns using column objects", example_5_column_select),
    6: ("Using comparison operators (>, <, >=, <=)", example_6_comparison_operators),
    7: ("Using IN operator for multiple values", example_7_in_operator),
    8: ("Grouping and aggregation with column objects", example_8_group_by),
    9: ("Ordering by column objects", example_9_order_by),
    10: ("Counting rows with column expressions", example_10_count),
    11: ("Getting first result", example_11_first),
    12: ("Checking if results exist", example_12_exists),
    13: ("Exporting to different formats", example_13_export_formats),
    14: ("Getting results as dictionary", example_14_dict_output),
    15: ("Iterating over results", example_15_iterate),
    16: ("Using NOT IN operator", example_16_not_in),
    17: ("Using LIKE operator", example_17_like),
    18: ("Complex OR expression", example_18_or_expression),
    19: ("Direct column access from table instance", example_19_direct_column_access),
    20: ("Time range queries with datetime objects", example_20_time_range),
    21: ("Multiple aggregations in select", example_21_multiple_aggregations),
    22: ("Using exchange and pair helper methods", example_22_helpers),
    23: ("Getting results as NumPy array", example_23_numpy),
    24: ("Exporting to CSV string", example_24_csv),
    25: ("Using inequality operators (!=, <, <=, >, >=)", example_25_inequality),
    26: ("String functions (length, upper, lower, substring)", example_26_string_functions),
    27: ("Date/time functions (toYear, toMonth, toHour)", example_27_date_time_functions),
    28: ("Math functions (abs, sqrt, round, floor, ceil)", example_28_math_functions),
    29: ("Conditional functions (if, coalesce)", example_29_conditional_functions),
    30: ("Type conversion functions (toString, toInt64, toFloat64)", example_30_type_conversion),
    31: ("String pattern matching (startsWith, endsWith)", example_31_string_pattern_matching),
    32: ("Combining multiple functions in one query", example_32_combined_functions),
    33: ("Window functions - basic with PARTITION BY", example_33_window_functions_basic),
    34: ("Window functions - ranking (rank, denseRank)", example_34_window_rank_functions),
    35: ("Window functions - LAG and LEAD", example_35_window_lag_lead),
    36: ("Window functions - ROWS BETWEEN frame", example_36_window_rows_between),
    37: ("Advanced aggregates (quantile, stddev)", example_37_advanced_aggregates),
    38: ("Correlation analysis", example_38_correlation_analysis),
    39: ("argMin and argMax functions", example_39_argmin_argmax),
    40: ("topK aggregate function", example_40_topk_groupby),
    41: ("Unique count functions (uniq, uniqExact)", example_41_unique_counts),
    42: ("Grouping into arrays (groupArray)", example_42_group_array),
    43: ("String replacement and manipulation", example_43_string_replace_functions),
    44: ("String extraction functions", example_44_string_extract_functions),
    45: ("Advanced date/time functions", example_45_date_time_advanced),
    46: ("Date arithmetic functions", example_46_date_arithmetic),
    47: ("Advanced mathematical functions (log, exp, pow)", example_47_math_advanced),
    48: ("Trigonometric functions", example_48_trigonometric_functions),
    49: ("Multi-conditional function (multiIf)", example_49_conditional_multiif),
    50: ("Null handling functions", example_50_null_handling),
    51: ("Basic array operations", example_51_array_basic_operations),
    52: ("Array manipulation functions", example_52_array_manipulation),
    53: ("Array filtering and mapping", example_53_array_filter_map),
    54: ("Subquery - EXISTS", example_54_subquery_exists),
    55: ("Subquery - IN subquery", example_55_subquery_in),
    56: ("Subquery - scalar subquery in SELECT", example_56_subquery_scalar),
    57: ("Subquery - derived table in FROM", example_57_subquery_from),
    58: ("JOIN - INNER JOIN example", example_58_join_inner),
    59: ("HAVING clause with expressions", example_59_having_with_expressions),
    60: ("Exporting to Parquet format", example_60_parquet_export),
    61: ("Running accumulation functions", example_61_running_functions),
    62: ("Neighbor function for adjacent rows", example_62_neighbor_function),
    63: ("Bid-ask spread analysis", example_63_price_spread_analysis),
    64: ("Time bucketing - aggregation by periods", example_64_time_bucketing),
    65: ("Format and encoding functions", example_65_format_functions),
}


# ============================================================================
# Interactive Mode Functions
# ============================================================================

def list_examples():
    """List all available examples with their numbers and names."""
    print("\n" + "=" * 70)
    print("Available Examples:")
    print("=" * 70)
    for num, (name, _) in sorted(EXAMPLES.items()):
        print(f"  {num:2d}. {name}")
    print("=" * 70)
    print("  0.  Run all examples")
    print("  q.  Quit")
    print("=" * 70 + "\n")


def run_example(example_num: int, client: ClickHouseClient, table: CryptoQuotesTable):
    """Run a specific example by number."""
    if example_num not in EXAMPLES:
        print(f"Error: Example {example_num} not found!")
        print(f"Available examples: {sorted(EXAMPLES.keys())}")
        return
    
    name, func = EXAMPLES[example_num]
    print("\n" + "=" * 70)
    print(f"Example {example_num}: {name}")
    print("=" * 70)
    try:
        func(table)
    except Exception as e:
        print(f"\nError running example: {e}")
        import traceback
        traceback.print_exc()
    print()


def interactive_mode():
    """Run examples in interactive mode."""
    print("\n" + "=" * 70)
    print("chpy Library - Interactive Example Runner")
    print("=" * 70)
    
    # Initialize the client
    try:
        client = ClickHouseClient(
            host="localhost",
            port=8123,
            username="default",
            password="",
            database="stockhouse"
        )
        table = CryptoQuotesTable(client)
        print("✓ Connected to ClickHouse\n")
    except Exception as e:
        print(f"✗ Failed to connect to ClickHouse: {e}")
        print("Please check your connection settings and try again.")
        return
    
    while True:
        list_examples()
        try:
            choice = input("Enter example number (or 'q' to quit): ").strip().lower()
            
            if choice == 'q' or choice == 'quit':
                print("\nGoodbye!")
                break
            elif choice == '0':
                print("\nRunning all examples...\n")
                for num in sorted(EXAMPLES.keys()):
                    run_example(num, client, table)
                print("=" * 70)
                print("All examples completed!")
                print("=" * 70)
            else:
                try:
                    example_num = int(choice)
                    run_example(example_num, client, table)
                except ValueError:
                    print(f"Invalid input: '{choice}'. Please enter a number or 'q'.\n")
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break
    
    client.close()


# ============================================================================
# Main Function (for running all examples)
# ============================================================================

def main():
    """Run all examples sequentially."""
    # Initialize the client
    client = ClickHouseClient(
        host="localhost",
        port=8123,
        username="default",
        password="",
        database="stockhouse"
    )
    
    # Create a wrapper for crypto_quotes table
    table = CryptoQuotesTable(client)
    
    print("=" * 70)
    print("chpy Library - ORM-Style Query Examples")
    print("=" * 70)
    print()
    
    # Run all examples
    for num in sorted(EXAMPLES.keys()):
        run_example(num, client, table)
    
    print("=" * 70)
    print("All examples completed!")
    print("=" * 70)
    
    # Close the connection
    client.close()


# ============================================================================
# Command Line Interface
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="chpy library examples - Interactive example runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python example.py              # Interactive mode
  python example.py --example 1   # Run example 1
  python example.py --all         # Run all examples
  python example.py --list        # List all examples
        """
    )
    parser.add_argument(
        '--example', '-e',
        type=int,
        help='Run a specific example by number (1-65)'
    )
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Run all examples'
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all available examples'
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_examples()
    elif args.example:
        # Run specific example
        client = ClickHouseClient(
            host="localhost",
            port=8123,
            username="default",
            password="",
            database="stockhouse"
        )
        table = CryptoQuotesTable(client)
        run_example(args.example, client, table)
        client.close()
    elif args.all:
        # Run all examples
        main()
    else:
        # Interactive mode (default)
        interactive_mode()
