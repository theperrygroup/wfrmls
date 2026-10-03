---
title: "Search WFRMLS properties"
description: "Search WFRMLS properties with filters, selected fields, price and city helpers, numeric listing identifiers, and Media expansion."
---

# Search WFRMLS properties

The `PropertyClient` helpers issue OData queries and return provider data.
Configure [authentication](../getting-started/authentication.md) first, and
use the current metadata to confirm field names and types.

## Combine filters in one query

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
response = client.property.get_properties(
    filter_query="City eq 'Provo' and ListPrice ge 300000 and ListPrice le 600000",
    select=["ListingId", "ListingKeyNumeric", "City", "ListPrice"],
    orderby="ListPrice asc,ListingKeyNumeric asc",
    top=25,
)
for record in response["value"]:
    print(record.get("ListingId"), record.get("ListPrice"))
```

`select` and `expand` accept a string or a list of strings. `filter_query` and
`orderby` are forwarded as strings. The library does not validate the fields
or convert plain strings into enum literals. If metadata declares a status
field as an enum, use the type-qualified literal required by that schema.
See [OData literals](odata-queries.md#build-filter-literals).

## Use convenience helpers carefully

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
response = client.property.get_properties_by_price_range(
    min_price=300000,
    max_price=600000,
    top=10,
    select=["ListingId", "ListPrice"],
)
print("Records on this page:", len(response["value"]))
```

The price helper builds inclusive `ListPrice ge` and `ListPrice le` conditions.
Do not also pass `filter_query` when a price bound is present: that method
already supplies the keyword and Python will reject a duplicate. Use
`get_properties()` when combining price bounds with other conditions.

`get_properties_by_city(city, **kwargs)` combines a city condition with an
optional `filter_query`, but it interpolates the city without escaping
apostrophes. For arbitrary user input, build an escaped literal explicitly:

```python
from wfrmls import WFRMLSClient

city = "O'Fallon"
city_literal = "'" + city.replace("'", "''") + "'"
client = WFRMLSClient()
response = client.property.get_properties(
    filter_query="City eq " + city_literal,
    top=10,
    select=["ListingId", "City"],
)
print("Records on this page:", len(response["value"]))
```

The `get_active_properties()` helper forwards `StandardStatus eq 'Active'`.
Its availability in the library does not ensure that the provider accepts
that literal or exposes all active listings to your account.

## Fetch details and media

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
record = client.property.get_property("1234567")
print(record.get("ListingId"), record.get("UnparsedAddress"))

response = client.property.get_properties(
    filter_query="ListingKeyNumeric eq 1234567",
    select=["ListingId", "ListingKeyNumeric"],
    expand="Media",
    top=1,
)
for record in response["value"]:
    for media in record.get("Media") or []:
        print(media.get("MediaURL"))
```

The single-property helper converts the identifier to an integer and requests
`Property(<number>)`; nonnumeric strings raise `ValidationError`. Its return
is an entity dictionary, while `get_properties()` returns a collection wrapper.

An expanded media collection may have its own continuation link; completing
the outer property collection alone does not establish that all media were
returned. OData defines these nested links in its
[JSON format](https://docs.oasis-open.org/odata/odata-json-format/v4.0/errata03/os/odata-json-format-v4.0-errata03-os-complete.html).
Confirm expansion support with your provider. This package has no `client.media`
service, and an accessible media URL does not grant unrestricted image use.
Review [data and media licensing](../legal/index.md).

## Read more than one page

`get_properties(top=25)` retrieves one page. The client caps `top` at 200;
that is a library limit, not a confirmed account quota. Validate positive
page sizes in your application.

`get_all_properties_paginated()` uses `$skip`, accumulates results in memory,
and returns accumulated records when any page raises an exception. Treat its
output as potentially partial. For workflows that need every page, use the
[next-link example](odata-queries.md#follow-collection-next-links), which
propagates failures. Avoid treating a page count or `@odata.count` alone as a
complete or stable snapshot of a changing feed.

## Next steps

Read [geographic-query limits](geolocation.md) before offering radius searches,
or [data synchronization](data-sync.md) before persisting a replicated dataset.
