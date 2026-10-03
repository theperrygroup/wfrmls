---
title: "Make your first WFRMLS request"
description: "Make your first WFRMLS property request, read OData collection records, fetch a single listing, and handle a failed service query."
---

# Make your first WFRMLS request

This guide queries a small property collection and explains the response shape.
Install the package and configure `WFRMLS_BEARER_TOKEN` using the
[installation](installation.md) and [authentication](authentication.md) guides
first. The examples make provider requests when run with real credentials.
For a version that runs without credentials or network access, use the
[offline example](../examples/index.md).

## Query a property collection

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
response = client.property.get_properties(
    top=5,
    select=["ListingId", "ListPrice", "City"],
    orderby="ListingKeyNumeric asc",
)

for record in response["value"]:
    print(record.get("ListingId"), record.get("ListPrice"), record.get("City"))
```

Collection methods return a dictionary, not a list. Iterate its `value` list.
Fields can be absent or `null`, particularly when you use `$select` or your
feed restricts access. Only request fields supported by the current metadata.

## Add a filter

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
response = client.property.get_properties(
    filter_query="City eq 'Salt Lake City' and ListPrice le 500000",
    top=10,
    select=["ListingId", "ListPrice", "City"],
    orderby="ListPrice asc,ListingKeyNumeric asc",
)
print("Matching records on this page:", len(response["value"]))
```

The library forwards the OData filter; the service validates field names,
types, and supported expressions. For string escaping and enum literals,
see [OData queries](../guides/odata-queries.md).

## Fetch a single property

`get_property()` accepts a numeric listing identifier and returns the property
dictionary directly. Replace the example identifier with one available to
your account:

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
record = client.property.get_property("1234567")
print(record.get("ListingId"), record.get("ListPrice"))
```

Do not index this result as `record["value"]`. The helper normalizes both a
direct entity response and the first record of a provider `value` wrapper.
An empty wrapper raises `NotFoundError`.

## Handle a service-query failure

```python
from wfrmls import WFRMLSClient
from wfrmls.exceptions import WFRMLSError

client = WFRMLSClient()
try:
    response = client.property.get_properties(top=1, select=["ListingId"])
except WFRMLSError as error:
    print("Property query failed; HTTP status:", error.status_code)
    raise
else:
    print("Records returned:", len(response["value"]))
```

No automatic retry occurs. Most service requests also have no explicit
timeout in the library. Review [error handling](../guides/error-handling.md)
and [rate limits](../guides/rate-limits.md) before running a scheduled workload.

## Explore other responses

`client.member.get_members(top=5)` and
`client.office.get_offices(top=5)` return collection dictionaries.
`client.get_service_document()` describes available resources, while
`client.get_metadata()` returns XML text. These are different response shapes;
consult the [client reference](../api/client.md).

## Next steps

Use [property search](../guides/property-search.md) for search composition and
media expansion. Use [paging](../guides/odata-queries.md#follow-collection-next-links)
when a response contains `@odata.nextLink`; one successful page does not
establish a complete result set.
