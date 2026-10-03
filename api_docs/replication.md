# Replication

This page preserves historical provider reference material. See the
[source and snapshot limitations](index.md#sources-and-snapshot-limits)
and [official provider documentation](https://docs.utahrealestate.com/).
Current account access and provider behavior have not been revalidated.

## Wrapper boundary

The patterns below describe provider pagination. The Python wrapper does not
persist checkpoints, schedule updates, reconcile a database, or automatically
follow `@odata.nextLink`. Its `get_all_properties_paginated()` helper uses
`$top`/`$skip`, collects results in memory, and catches page-fetch exceptions;
a returned result can therefore be partial. Do not use that result alone as
proof of a complete scan. See the [Python synchronization guide](../docs/guides/data-sync.md)
and [property API reference](../docs/api/properties.md).

## Pulling data

For an initial import, request records accessible to the vendor account. The
retained provider guide describes continuation links, offset paging, and
numeric-key paging. None establishes a transactionally consistent snapshot of
a changing provider dataset.

The retained guide recommends following the response's `@odata.nextLink` for
subsequent pages. Persist each successfully fetched page and follow the supplied
continuation until none is returned. A request error must fail the scan rather
than be interpreted as an empty final page. The wrapper's `BaseClient.get()`
expects a relative endpoint and does not accept an absolute continuation URL as
a ready-to-follow URL; an application needs its own trusted provider continuation
handling.

For example, to replicate all Property records, make the initial request to the Property endpoint.

`https://resoapi.utahrealestate.com/reso/odata/Property`

Illustrative abbreviated response with a continuation link:

```json
{
    "@odata.context": "$metadata#Property",
    "value": [{"ListingKeyNumeric": 11031}],
    "@odata.nextLink": "https://resoapi.utahrealestate.com/reso/odata/Property?$skip=200"
}
```

Continue this pattern until all records have been pulled.

Alternatively, use **$top** for a requested page size and **$skip** for an offset.
The retained examples use 200-record pages; current provider page sizes may vary
by vendor configuration. This is separate from a requests-per-second limit.

For example, to get started replicating listings:

`https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ListingKeyNumeric&$top=200`

`https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ListingKeyNumeric&$top=200&$skip=200`

`https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ListingKeyNumeric&$top=200&$skip=400`

etc.

Continue this pattern until the API no longer returns results, or until the number of replicated listings matches the count. See [query options](query-options.md#count) for counts. Counts can change during
a scan and do not replace checking every page for request errors.

Using the **$skip** option to paginate over large data sets can be time consuming. Especially when ordering by a non numeric, or non indexed field. As the **$skip** value gets larger, query response time may slow down. If paginating through a large data set, it is advised to order by the primary key, or an indexed field. For example, if replicating the entire Property resource, the historical guide recommends ordering by `ListingKeyNumeric`. Actual
performance depends on the provider and query.

## PHP offset example

The following PHP example demonstrates offset paging with fake credentials.
The database operation is a placeholder; checkpoint persistence and consistent
scan validation must be supplied by the application.

```php
/* Get your Bearer token from the vendor details page */

$token = 'YourBearerToken';

/* Create the base url for the Property resource */

$url = 'https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ListingKeyNumeric';

/* Apply any filters (ie. Active Residential). Skip this if you want all listings */

$filters = array("StandardStatus eq Odata.Models.StandardStatus'Active'", "PropertyType eq Odata.Models.PropertyType'Residential'");

$url .= '&$filter=' . implode(' and ', $filters);

/* Apply the $top option. This is the number of listings that can be pulled in one request.
This value may vary depending on vendor configuration
*/

$top = 200;

$url .= '&$top=' . $top;

/* Create a function for making the request */

function getResponse($url, $token){

    $opts = [
        "http" => [
            "method" => "GET",
            "header" => "Authorization: Bearer $token\r\nAccept: application/json"
        ]
    ];

    $context = stream_context_create($opts);

    $url = str_replace(" ", "%20", $url);    //make sure white spaces are encoded

    $response = file_get_contents($url, false, $context);
    if ($response === false) {
        throw new RuntimeException('Provider request failed; scan is incomplete');
    }

    $json = json_decode($response, true);
    if (!is_array($json) || !isset($json['value']) || !is_array($json['value'])) {
        throw new RuntimeException('Invalid provider page; scan is incomplete');
    }

    return $json;
}

/* Start at offset 0 and advance by the number of records actually returned. */

$skip = 0;

do{

    $request_url = $url . '&$skip=' . $skip;

    $json = getResponse($request_url, $token);

    $listings = $json['value'];

    foreach($listings as $listing){

        // Persist $listing successfully before advancing this page checkpoint.
    }

    $skip += count($listings);

}while(count($listings) > 0);
```

## Numeric-key paging

Using the **$skip** option to paginate over large data sets can be time consuming. As the **$skip** value gets larger, query response time may slow down. The historical guide offers **$filter** with a numeric primary key as an
alternative to large offsets. Use a stable, unique key in ascending order and
advance it only after successfully persisting the page.

For example:

1. Make the initial query. Make sure to order by the primary key:
   https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ListingKeyNumeric&$top=200
2. After replicating each row, record the primary key of the last row. In this case, ListingKeyNumeric.
3. Use the recorded key from the last query in a $filter to get the next 200 rows.
   https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ListingKeyNumeric&$top=200&$filter=ListingKeyNumeric gt 11031
4. Repeat step 2 and 3 until all rows have been replicated.

The following PHP example demonstrates numeric-key paging without `$skip`.
No current performance multiplier is established by this review. As in the
offset example, database persistence is a placeholder. These are alternative
standalone snippets; do not paste both `getResponse()` declarations into one
PHP program.

```php
/* Get your Bearer token from the vendor details page */

$token = 'YourBearerToken';

/* Create the base url for the Property resource. Make sure to order by the primary key */

$url = 'https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ListingKeyNumeric';

/* Apply the $top option. This is the number of listings that can be pulled in one request.
This value may vary depending on vendor configuration
*/

$top = 200;

$url .= '&$top=' . $top;

/* Create a function for making the request */

function getResponse($url, $token){

    $opts = [
        "http" => [
            "method" => "GET",
            "header" => "Authorization: Bearer $token\r\nAccept: application/json"
        ]
    ];

    $context = stream_context_create($opts);

    $url = str_replace(" ", "%20", $url);    //make sure white spaces are encoded

    $response = file_get_contents($url, false, $context);
    if ($response === false) {
        throw new RuntimeException('Provider request failed; scan is incomplete');
    }

    $json = json_decode($response, true);
    if (!is_array($json) || !isset($json['value']) || !is_array($json['value'])) {
        throw new RuntimeException('Invalid provider page; scan is incomplete');
    }

    return $json;
}

/* $last_key will record the primary key of the last row replicated, in this case ListingKeyNumeric */

$last_key = 0;

do{

    $request_url = $url;

    if($last_key > 0){

        $request_url .= '&$filter=ListingKeyNumeric%20gt%20' . $last_key;
    }

    $json = getResponse($request_url, $token);

    $listings = $json['value'];

    foreach($listings as $listing){

        // Persist $listing successfully before advancing this page checkpoint.
    }

    $last_row = end($listings);

    if (!empty($last_row)) {
        if (!isset($last_row['ListingKeyNumeric']) ||
            !is_numeric($last_row['ListingKeyNumeric']) ||
            $last_row['ListingKeyNumeric'] <= $last_key) {
            throw new RuntimeException('Invalid or non-advancing page key');
        }
        $last_key = $last_row['ListingKeyNumeric'];
    }

}while(count($listings) > 0);
```

## Keeping data up to date

The retained provider material recommends 15-minute incremental pulls. Confirm
the appropriate frequency and limits for the current vendor account. The Python
wrapper supplies request helpers, not a scheduler or a persisted sync state.

Use a durable UTC checkpoint, process every page successfully, and advance the
checkpoint only after storing the full intended update window. Allow for records
sharing a timestamp and changes arriving during a scan; an application may need
a bounded window and overlap with idempotent updates.

Use **$filter** on `ModificationTimestamp` to request changed records, and
process all returned pages.

For example, this historical query asks for records modified after September 1,
2019 at 10:00 UTC:

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=ModificationTimestamp gt 2019-09-01T10:00:00Z`

```http
GET /reso/odata/Property?$filter=ModificationTimestamp%20gt%202019-09-01T10:00:00Z HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

Sorting by `ModificationTimestamp desc` retrieves a recent page, but does not
ensure that every change since the checkpoint has been fetched. It is unsuitable
as the sole incremental replication strategy:

`https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ModificationTimestamp desc`

```http
GET /reso/odata/Property?$orderby=ModificationTimestamp%20desc HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

## Deleted records and access reconciliation

The retained guide distinguishes provider deletions from records that become
unavailable to a vendor. Reconcile records according to your licensing and
retention requirements, with a validated complete scan where one is needed.

The historical `Deleted` endpoint reports records removed from the API. The
wrapper exposes `client.deleted`; see the [Deleted API reference](../docs/api/deleted.md).

`https://resoapi.utahrealestate.com/reso/odata/Deleted`

```http
GET /reso/odata/Deleted HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

The query results will show the deleted resource, the primary key of the deleted row, and the date/time the record was removed.

```json
{
    "@odata.context": "$metadata#Deleted",
    "value": [
        {
            "resource": "OpenHouse",
            "primary_key": "337211",
            "ts": "2020-07-30T08:55:07Z"
        },
        {
            "resource": "OpenHouse",
            "primary_key": "337269",
            "ts": "2020-07-30T08:55:07Z"
        }
    ]
}
```

OData **$filter** options can be used to refine your search for deleted records. For example:

Get all deleted Property records.

`https://resoapi.utahrealestate.com/reso/odata/Deleted?$filter=resource eq 'Property'`

Get all open houses deleted since a given date.

`https://resoapi.utahrealestate.com/reso/odata/Deleted?$filter=resource eq 'OpenHouse' and ts gt 2020-07-01T01:00:00Z`

The 'Deleted' resource only applies to records that have been removed from the API. It does not apply to a record that becomes unavailable to the vendor through a status change or other restriction.

A full **$select** scan of keys can identify records no longer visible to the
account. Treat absence as an access reconciliation signal, not proof of a
provider deletion. Only act on missing keys after every page has succeeded and
the scan has been validated; a partial response, changed filter, changed access,
or request failure must not trigger bulk removal.

For example, collect `ListingKeyNumeric` with the same account and scope as the
local dataset, following every page. Compare the completed inventory with local
keys and apply the application's authorized reconciliation policy. The requests
below illustrate offset paging only; three pages are not a full inventory:

`https://resoapi.utahrealestate.com/reso/odata/Property?$top=200&$select=ListingKeyNumeric`

`https://resoapi.utahrealestate.com/reso/odata/Property?$top=200&$skip=200&$select=ListingKeyNumeric`

`https://resoapi.utahrealestate.com/reso/odata/Property?$top=200&$skip=400&$select=ListingKeyNumeric`

etc.

See [query options](query-options.md) for paging and field selection, and
[OData endpoints](odata-endpoints.md#metadata) for key types in the schema snapshot.
