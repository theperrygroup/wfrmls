---
description: Construct standalone HistoryTransactionalClient queries for property transactions, sale price and date filters, closed records, and modification cutoffs.
---

# Standalone transaction-history queries

`HistoryTransactionalClient` remains exported from `wfrmls`. It is a standalone compatibility class: `WFRMLSClient` has no `history` attribute. The interface is covered by mocked request tests; current provider availability and account access have not been verified.

## Construct the client and query a page

`HistoryTransactionalClient(bearer_token=None, base_url=None)` requires an explicit token or `WFRMLS_BEARER_TOKEN` at construction. Missing credentials raise `AuthenticationError`. Shared transport and response behavior is described in [BaseClient](base-client.md).

`get_history_transactions(top=None, skip=None, filter_query=None, select=None, orderby=None, expand=None, count=None)` requests the `HistoryTransactional` collection. It returns handled provider JSON, commonly a dictionary with `value`.

| Parameter | Type | Default | Request behavior |
| --- | --- | --- | --- |
| `top` | `int \| None` | `None` | `$top`; values above 200 are clamped |
| `skip` | `int \| None` | `None` | `$skip`, unchanged |
| `filter_query` | `str \| None` | `None` | Raw `$filter` |
| `select` | `list[str] \| str \| None` | `None` | `$select`; lists are joined with commas |
| `orderby` | `str \| None` | `None` | Raw `$orderby` |
| `expand` | `list[str] \| str \| None` | `None` | `$expand`; lists are joined with commas |
| `count` | `bool \| None` | `None` | Lowercase `$count` value |

Omitted arguments are not sent. There is no automatic pagination, date validation, filter escaping, or guarantee that the server accepts the named fields.

This mocked example checks an inclusive sale-date filter without a provider call:

```python
from datetime import date
from unittest.mock import patch
from wfrmls import HistoryTransactionalClient

with patch.object(HistoryTransactionalClient, "get", return_value={"value": []}) as request:
    history = HistoryTransactionalClient(bearer_token="example-token")
    response = history.get_sales_by_date_range(
        date(2026, 1, 1), date(2026, 1, 31), top=10
    )
    assert response == {"value": []}
    request.assert_called_once_with(
        "HistoryTransactional",
        params={
            "$top": 10,
            "$filter": (
                "TransactionType eq 'Sale' and CloseDate ge '2026-01-01' "
                "and CloseDate le '2026-01-31'"
            ),
        },
    )
```

## Transaction and sale helpers

| Method | Parameters and defaults | Request behavior |
| --- | --- | --- |
| `get_history_transaction` | `transaction_key: str` | Quoted key URL `HistoryTransactional('<key>')`, without response normalization |
| `get_transactions_for_property` | `listing_key: str`, `**kwargs` | Quoted `ListingKey` filter |
| `get_sales_by_price_range` | `min_price=None`, `max_price=None`, `**kwargs` | Sale type plus inclusive `ClosePrice ge/le` bounds |
| `get_sales_by_date_range` | `start_date`, `end_date`, `**kwargs` | Sale type plus inclusive quoted `CloseDate ge/le` bounds |
| `get_recent_sales` | `days_back=30`, `**kwargs` | Sale type and `CloseDate ge` a local naive datetime cutoff |
| `get_transactions_by_city` | `city: str`, `**kwargs` | Quoted `City` filter |
| `get_closed_transactions` | `**kwargs` | `Status eq 'Closed'` |
| `get_transactions_with_property` | `**kwargs` | `$expand=Property` |
| `get_modified_transactions` | `since: str \| date \| datetime`, `**kwargs` | Quoted `ModificationTimestamp gt` cutoff |

Except for the single-key lookup, these helpers return one collection response. Property, price, date, recent-sale, and city helpers combine an existing `filter_query` with `and` without added grouping. They do not calculate market trends or retrieve every sale.

`start_date` and `end_date` accept strings, dates, or datetimes. Dates and datetimes use `isoformat()`; strings are unchanged, and the bounds are quoted. `get_recent_sales()` subtracts days from local `datetime.now()`, without UTC conversion.

## Modification and fixed-keyword limits

`get_modified_transactions()` sends strings unchanged, expands dates to midnight with `Z`, and appends `Z` to datetime `isoformat()` without converting its timezone. Prefer a normalized UTC string; an aware datetime can produce two timezone designators.

Do not pass `filter_query` to `get_closed_transactions()` or `get_modified_transactions()`, or `expand` to `get_transactions_with_property()`. Those helpers supply the keyword themselves; duplicate keywords raise `TypeError`. Other `**kwargs` must match `get_history_transactions()`.

Keys and string filter values are interpolated without escaping. `HistoryTransactionType` and `HistoryStatus` contain package constants; they do not certify current provider values. Pass `.value` when using them as filter text.

See [compatibility clients](unavailable-clients.md), [provider verification](live-api-updates.md), and [response conventions](../reference/index.md).

## Generated signatures and constants

::: wfrmls.history
    options:
      show_root_heading: false
      show_source: false
