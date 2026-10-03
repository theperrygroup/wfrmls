---
description: Understand WFRMLSAnalytics sampled listing summaries, price segments, agent reports, data-quality scores, error dictionaries, and current limitations.
---

# Analytics over sampled WFRMLS records

`WFRMLSAnalytics(client)` calculates summaries from property and member responses. It does not request a provider analytics endpoint or paginate through the full market.

## Construct the analytics helper

```python
from wfrmls import WFRMLSAnalytics, WFRMLSClient

analytics = WFRMLSAnalytics(WFRMLSClient())
summary = analytics.get_market_summary(city="Salt Lake City", days_back=30)
if "error" in summary:
    print(summary["error"])
else:
    print(summary["inventory"]["active_listings"])
    print(summary["pricing"]["median_price"])
```

Configure `WFRMLS_BEARER_TOKEN` before the first service access. Check for `error` before reading report-specific keys: the helpers catch exceptions and return an error dictionary.

## Compare the report methods

| Method | Parameters and defaults | Result sections |
| --- | --- | --- |
| `get_market_summary` | `city=None`, `days_back=30`, `property_type=None` | `inventory`, `pricing`, `activity` |
| `analyze_price_trends` | `city=None`, `days_back=90`, `property_type=None`, `price_segments=5` | `overall_pricing`, `price_segments`, `market_insights` |
| `generate_agent_performance_report` | `days_back=90`, `min_listings=5` | `summary`, `top_agents`, sample counts |
| `get_data_quality_report` | No parameters | `property_quality`, `member_quality`, score, issues |

### Listing summary

`get_market_summary()` requests up to 200 active listings and another 200 active listings filtered by `ListingContractDate`. It summarizes the records returned, rather than a server-side count or completed sales. Prices use truthy `ListPrice` values; days on market are computed from parseable contract dates.

The result includes `market_area`, `property_type`, `analysis_period`, `timestamp`, and:

- `inventory`: `active_listings`, `new_listings`, and `new_listings_rate`.
- `pricing`: mean, median, minimum, maximum, and price range.
- `activity`: average computed days on market, the number of dated records, and `market_velocity` (`30 / average days`).

The date filter currently appends `Z` to an offset-bearing UTC string, producing text such as `...+00:00Z`. A server may reject it; the helper then returns `error`. This is an implementation limitation, not evidence of current provider behavior.

### Price segments, rather than a time series

`analyze_price_trends()` makes one Active-listing request for at most 200 records, selects price/size/date fields, and groups positive prices into sorted segments. `days_back` labels the report but is not used in a date filter. The result is a sampled price distribution, not historical appreciation or a period-over-period trend.

Use a positive `price_segments` no larger than the number of valid priced records. Empty segments cause an error dictionary. Missing/zero-size records are excluded from price-per-square-foot calculations.

### Agent activity sample

`generate_agent_performance_report()` requests up to 200 recent property records with `Member` expansion and up to 200 active members. It matches `MemberKey`, aggregates by `MemberFullName`, excludes agents below `min_listings`, and returns the top 10 by listing count, total list value, and mean list price.

This is not a commission, closed-sales, or complete agent-performance report. Members sharing a display name can be grouped together. Its contract-date filter has the same `+00:00Z` limitation as the listing summary.

### Data completeness sample

`get_data_quality_report()` checks up to 50 properties and 30 members. Falsey price, city, bedroom, size, and email values count as missing. It returns `GOOD` above 0.9, `FAIR` above 0.7, otherwise `NEEDS_ATTENTION`.

An empty property sample causes a division-by-zero error that is returned in the `error` dictionary. The report does not inspect office records, validate source accuracy, or certify data quality beyond these selected fields.

## Generated signatures and return details

::: wfrmls.analytics.WFRMLSAnalytics
    options:
      show_root_heading: false
      show_source: false

See [property queries](properties.md) for OData behavior and [exceptions](exceptions.md) for failures that other client methods raise directly.
