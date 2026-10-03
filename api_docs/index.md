# UtahRealEstate.com Provider API Reference

This directory preserves provider-oriented documentation checked into the
WFRMLS Python client repository. It describes UtahRealEstate.com's RESO/OData
API protocol and historical examples; the [Python client API reference](../docs/api/index.md)
describes the wrapper's implemented methods.

## Sources and snapshot limits

The original index identifies the material as scraped from the
[vendor dashboard](https://vendor.utahrealestate.com/), but does not record a
capture date. Example responses contain 2019–2020 dates, and the retained
[provider change log](change-log.md) ends in April 2021. These dates establish
historical context, not a complete account of subsequent provider changes.

Consult the [official provider documentation](https://docs.utahrealestate.com/)
and your vendor account for current resource access, schema, page sizes, and
request limits. During the October 2, 2026 documentation review, the official
docs host did not resolve from the review environment; the vendor dashboard
also could not be read through the public fetch tool. Current provider behavior
has therefore **not** been revalidated by this review. The checked-in
[metadata.xml](metadata.xml) is a schema snapshot with no verified capture date;
it is not the authenticated account's current `$metadata` response.

## Provider reference pages

| Page | What it explains |
| --- | --- |
| [Overview](overview.md) | Historical API context, vendor access, and bearer headers. |
| [OData endpoints](odata-endpoints.md) | Service documents, metadata, and resource discovery. |
| [Query options](query-options.md) | Selection, filters, paging, counts, and related resources. |
| [Geolocation search](geolocation-search.md) | Historical spatial syntax and the wrapper's explicit limitation. |
| [Replication](replication.md) | Provider pagination patterns, incremental updates, and deletion reconciliation. |
| [Getting photos](getting-photos.md) | Media expansion and historical direct Media queries. |
| [Getting open houses](getting-open-houses.md) | OpenHouse queries and timezone interpretation. |
| [Addresses](addresses.md) | Standard addresses and Utah grid address fields. |
| [Provider change log](change-log.md) | Retained 2020–2021 provider changes. |

## Protocol and wrapper boundaries

The wrapper's default service root is
`https://resoapi.utahrealestate.com/reso/odata`. Authenticate HTTP requests with
`Authorization: Bearer <token>`; Python constructors accept `bearer_token` or
use `WFRMLS_BEARER_TOKEN` when the underlying service client initializes.

- `WFRMLSClient` exposes Property, Member, Office, OpenHouse, DataSystem,
  Resource, PropertyUnitTypes, Lookup, Adu, and Deleted resource clients.
- Media, HistoryTransactional, and PropertyGreenVerification appear in the
  historical provider material and have standalone Python classes, but there
  are no `client.media`, `client.history`, or `client.green_verification`
  accessors in the current main client. A provider resource listing does not
  establish present availability.
- The wrapper's radius and polygon helpers raise `ValidationError` before
  sending a request. The historical provider spatial examples are not working
  Python helper examples.
- The property collection method caps a supplied `top` at 200. A page size is
  different from a requests-per-second rate limit; this directory does not
  establish a current provider request quota.
- The historical provider material recommends 15-minute incremental pulls.
  The wrapper has no scheduler, and that recommendation is not a verified
  current contract for every vendor account.
- The wrapper's property pagination helper uses `$top` and `$skip`, not
  `@odata.nextLink`, and can return partial data after an exception. Confirm
  completeness before using a scan for reconciliation or removal decisions.

Use the [getting-started guide](../docs/getting-started/index.md) for Python
setup and the [data synchronization guide](../docs/guides/data-sync.md) for
application-level patterns. Provider response examples here are illustrative
snapshots, not current listing records or contractual guarantees.
