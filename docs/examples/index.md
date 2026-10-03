---
title: "Runnable WFRMLS examples"
description: "Run an offline mocked WFRMLS property query, verify the value response shape, and find focused examples for paging, retries, and synchronization."
---

# Runnable WFRMLS examples

Start with this offline example to verify the client call and collection shape
without a real token or provider request. The remaining guides show focused
application patterns rather than complete production integrations.

## Run a mocked property query

Install the optional test dependency in your environment:

```bash
python -m pip install wfrmls responses
```

Save the following as `mocked_search.py` and run `python mocked_search.py`.
`responses` intercepts Requests calls and rejects unregistered URLs while its
context is active. The token and listing below are intentionally synthetic.

```python
import responses

from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token="documentation-test-token")
with responses.RequestsMock() as mock:
    mock.add(
        responses.GET,
        "https://resoapi.utahrealestate.com/reso/odata/Property",
        json={
            "value": [
                {"ListingId": "1234567", "City": "Example City", "ListPrice": 400000}
            ]
        },
        status=200,
    )
    response = client.property.get_properties(
        top=1,
        select=["ListingId", "City", "ListPrice"],
    )
    assert len(response["value"]) == 1
    print(response["value"][0]["ListingId"])
```

Expected output:

```text
1234567
```

A collection is a dictionary containing a `value` list. Iterating the outer
dictionary would iterate its keys. By contrast, `get_property()` returns the
normalized entity dictionary directly.

## Find an example for your task

| Task | Example and limits |
| --- | --- |
| Query live data | [Quick start](../getting-started/quickstart.md); requires authorized provider credentials. |
| Compose a search | [Property search](../guides/property-search.md); verifies helper parameters and string escaping. |
| Read every page | [OData paging](../guides/odata-queries.md#follow-collection-next-links); includes an application helper with timeouts and origin checks. |
| Retry a failed read | [Error handling](../guides/error-handling.md#add-bounded-retries-for-reads); bounded attempts for selected library exceptions. |
| Keep a checkpoint | [Synchronization](../guides/data-sync.md); stages updates and advances state only after a complete fetch. |
| Check radius support | [Geographic limitations](../guides/geolocation.md); demonstrates the local validation failure. |

Mocks validate application behavior against the chosen fixture. They do not
verify current provider field types, feed permissions, quotas, or MLS licensing.
Use the provider's metadata and your agreement for those contracts.
