---
description: Interpret WFRMLS OData collections, single-record responses, extracted lists, JSON metadata, timestamp filters, counts, and pagination limits.
---

# WFRMLS response and query conventions

The package usually returns parsed provider JSON without transforming its field names. The result shape depends on the method you call.

## Collection and single-record responses

A collection example is illustrative, not a captured provider response:

```json
{
  "@odata.context": "https://resoapi.utahrealestate.com/reso/odata/$metadata#Property",
  "value": [{"ListingId": "12345", "ListPrice": 450000}],
  "@odata.count": 1234
}
```

`value` contains returned records. `@odata.count` is optional and can describe the total matching collection rather than this page. `@odata.context` and `@odata.nextLink` are also server-provided; their presence is not guaranteed.

| Method family | Return shape |
| --- | --- |
| Collection `get_*` queries | JSON dictionary, commonly with `value` |
| `PropertyClient.get_property()` | Single object, normalizing a wrapped first item |
| Other key lookup methods | Parsed JSON, without shared single-record normalization |
| `WFRMLSClient.get_metadata()` | XML string |
| `LookupClient.get_lookup_names()` | JSON collection selecting `LookupName`, without deduplication |
| `MediaClient.get_media_urls_for_property()` | List of URL strings |
| `MediaClient.get_primary_photo()` | First object or `None` |
| Analytics helpers | Report dictionary or dictionary with `error` |
| `DeletedClient.get_all_deleted_for_sync()` | Aggregate dictionary with `value`, `by_resource`, and `sync_info` |

Most helpers do not retrieve every page. See each [API reference](../api/index.md) before treating a list, summary, or collection as complete.

## Named OData parameters

Resource collection methods accept `top`, `skip`, `filter_query`, `select`, `orderby`, `expand`, and `count`. Convenience methods can set some of those options themselves; use the specific method's signature.

| Python argument | Request parameter | Conversion |
| --- | --- | --- |
| `top` | `$top` | Most collection clients clamp values above 200 |
| `skip` | `$skip` | Sent unchanged |
| `filter_query` | `$filter` | Sent as supplied |
| `select` | `$select` | Lists joined with commas |
| `orderby` | `$orderby` | Sent as supplied |
| `expand` | `$expand` | Lists joined with commas |
| `count` | `$count` | Lowercase `true`/`false` |

`None` omits a parameter. Passing `filter`, `limit`, `fields`, or arbitrary keywords to these methods is not supported. Convenience helpers accepting `**kwargs` still delegate to a fixed collection signature.

Field names and string values are case-sensitive server data. The wrapper does not validate or escape raw filters. For example, an apostrophe inside an OData string literal must be doubled before you construct the expression. Enum constants must be converted with `.value` where a helper expects strings.

## Property keys and field names

`get_property(listing_id)` uses `int(listing_id)` to form `Property(<number>)`; it is not a general `ListingKey` string lookup. Other resource key methods construct their own quoted or numeric URLs.

Common fields used by implemented helpers include `ListPrice`, `StandardStatus`, `City`, `BedroomsTotal`, `BathroomsTotalInteger`, `LivingArea`, and `ModificationTimestamp`. These names describe request construction, not a guarantee that every account or selected record includes those fields. Inspect [metadata](../api/client.md#discover-entity-sets-and-field-definitions) for your schema and use `.get()` for optional response fields.

## Dates, filters, and location queries

Prefer a UTC ISO datetime string with one timezone designator, such as `2026-01-01T00:00:00Z`. Timestamp formatting differs by helper: some append `Z`, some quote dates, and some send strings unchanged. Read the specific method rather than assuming universal normalization.

For combined expressions, add parentheses when operator precedence matters. Helper-generated expressions are generally joined with `and` without extra grouping.

The package's radius and polygon searches are disabled, and its address helper only extracts a city. There is no automatic geocoding or distance calculation. See [property location limitations](../api/properties.md#location-helper-limitations).

## Pagination and errors

Single collection calls return one page and do not automatically follow next links. Property pagination uses `$skip` offsets and can return partial data after a swallowed error. The multi-resource deleted-record helper represents failed resources with empty lists and no error marker. Counts, successful-looking dictionaries, and helper summaries do not prove a complete replication.

Shared HTTP handling maps failures to [custom exceptions](../api/exceptions.md), but metadata and analytics use different failure paths. There is no automatic retry or rate-limit backoff.

See [HTTP client behavior](../api/base-client.md), [property queries](../api/properties.md), and [data synchronization](../guides/data-sync.md).
