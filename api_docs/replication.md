# Replication

## Replication

### Pulling Data

To get started you will want to pull all records in the system. This can be done three different ways.

The easiest way to repliate would be to follow the 'nextLink' at the bottom of each result set. This link can be followed to get the next page of results. Continue following the 'nextLink' until it no longer appears, or the API no longer returns a result set.

For example, to replicate all Property records, make the initial request to the Property endoint.

`https://resoapi.utahrealestate.com/reso/odata/Property`

Next, save the results to your database and look for the 'nextLink'

```json
{
    "@odata.context": "$metadata#Property",
    "value": [ .... ],
    "@odata.nextLink": "https://resoapi.utahrealestate.com/reso/odata/Property?$skip=200"
}
```

Continue this pattern until all records have been pulled.

Alternatively, replication can also be done by making requests to the endpoint using the query options **$top** and **$skip** The web API has a limit on how many records can be pulled at once. Currently, the default limit is set to 200 records per request. The **$top** and **$skip** query options can be used to offset the result set.

For example, to get started replicating listings:

`https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ListingKeyNumeric&$top=200`

`https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ListingKeyNumeric&$top=200&$skip=200`

`https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ListingKeyNumeric&$top=200&$skip=400`

etc.

Continue this pattern until the API no longer returns results, or until the number of replicated listings matches the count. See Query Options for how to get the count.

Using the **$skip** option to paginate over large data sets can be time consuming. Especially when ordering by a non numeric, or non indexed field. As the **$skip** value gets larger, query response time may slow down. If paginating through a large data set, it is advised to order by the primary key, or an indexed field. For example, if replicating the entire Property resource, ordering by ListingKeyNumeric would be the fastest.

### PHP example

The following is an example of full listing replication using PHP.

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
            "header" => "Authorization: Bearer $token"
        ]
    ];

    $context = stream_context_create($opts);

    $url = str_replace(" ", "%20", $url);    //make sure white spaces are encoded

    $response = file_get_contents($url, false, $context);

    return $response;
}

/* Start the $skip option at 0. This is the offset and needs to be incremented by the value in $top with each request. */

$skip = 0;

do{

    $request_url = $url . '&$skip=' . $skip;

    $response = getResponse($request_url, $token);

    $json = json_decode($response, true);

    $listings = $json['value'];

    foreach($listings as $listing){

        //write or update $listing to db
    }

    $skip += $top;

}while(count($listings) > 0);
```

### Faster Replication

Using the **$skip** option to paginate over large data sets can be time consuming. As the **$skip** value gets larger, query response time may slow down. A faster alterative to using **$skip** would be to use the **$filter** option in combination with a numeric primary key.

For example:

1. Make the initial query. Make sure to order by the primary key:  
   https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ListingKeyNumeric&$top=200
2. After replicating each row, record the primary key of the last row. In this case, ListingKeyNumeric.
3. Use the recorded key from the last query in a $filter to get the next 200 rows.  
   https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ListingKeyNumeric&$top=200&$filter=ListingKeyNumeric gt 11031
4. Repeat step 2 and 3 until all rows have been replicated.

The following is an example of full listing replication without $skip using PHP. It is on average 4 times faster than the methods listed above.

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
            "header" => "Authorization: Bearer $token"
        ]
    ];

    $context = stream_context_create($opts);

    $url = str_replace(" ", "%20", $url);    //make sure white spaces are encoded

    $response = file_get_contents($url, false, $context);

    return $response;
}

/* $last_key will record the primary key of the last row replicated, in this case ListingKeyNumeric */

$last_key = 0;

do{

    $request_url = $url;

    if($last_key > 0){

        $request_url .= '&$filter=ListingKeyNumeric%20gt%20' . $last_key;
    }

    $response = getResponse($request_url, $token);

    $json = json_decode($response, true);

    $listings = $json['value'];

    foreach($listings as $listing){

        //write or update $listing to db
    }

    $last_row = end($listings);

    if(!empty($last_row)){

        $last_key = $last_row['ListingKeyNumeric'];
    }

}while(count($listings) > 0);
```

### Keeping up-to-date

To keep your records up-to-date you will need to make frequent requests to the API to get the latest changes. We recommend making an update request every 15 minutes.

To get the latest changes use the **$filter** option to restrict records by their ModificationTimestamp.

For example, if your last pull/update was on 9/01/2019 at 10am, you would want all records that have been updated since then.

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=ModificationTimestamp gt 2019-09-01T10:00:00Z`

```http
GET /reso/odata/Property?$filter=ModificationTimestamp%20gt%202019-09-01T10:00:00Z HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

You could also use the $orderby query option to get the 200 most recent records.

`https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ModificationTimestamp desc`

```http
GET /reso/odata/Property?$orderby=ModificationTimestamp%20desc HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

### Deleting old Data

If a record is removed from the system it may be necessary to purge old data from your database.

You can use the 'Deleted' endpoint to query resources that have been deleted

`https://resoapi.utahrealestate.com/reso/odata/Deleted`

```http
GET /reso/odata/Deleted HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
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

You can also use the **$select** query option to get just the primary keys for a resource and then delete any records in your database that are not in the list of keys.

For example, to remove all old properties the process would be similar to the "Pull" example above, but you would only be collecting the ListingKey, or ListingKeyNumeric. Once you have collected all ListingKeys you can delete the properties in your database that are not included in that list.

`https://resoapi.utahrealestate.com/reso/odata/Property?$top=200&$select=ListingKeyNumeric`

`https://resoapi.utahrealestate.com/reso/odata/Property?$top=200&$skip=200&$select=ListingKeyNumeric`

`https://resoapi.utahrealestate.com/reso/odata/Property?$top=200&$skip=400&$select=ListingKeyNumeric`

etc. 