# Web API Documentation

This page preserves historical provider reference material. See the
[source and snapshot limitations](index.md#sources-and-snapshot-limits)
and [official provider documentation](https://docs.utahrealestate.com/).
Current account access and provider behavior have not been revalidated.

## Introduction

The retained material describes UtahRealEstate.com's Web API as an OData v4.0 REST API with RESO Web API and Data Dictionary certification. This is historical provider context, not a claim about a current certification version or the Python package's certification.

## What is a REST API?

REST stands for Representational State Transfer. This is an architectural pattern describing how distributed systems can expose a consistent interface. When the term is used, it generally refers to an API accessed via HTTP protocol at a predefined set of URLs.

These URLs represent various resources - any information or content accessed at that location, which can be returned as JSON, HTML, audio files, or images. REST APIs can define methods such as GET, POST, PUT, and DELETE. This wrapper exposes read-oriented resource methods; this general protocol description does not establish provider write permissions or implemented Python write methods.

## Getting Started

The retained onboarding instructions direct vendors to a data services account and its Service Details page for a bearer token and permitted resources. Confirm the current registration process and licensing requirements with the provider.

[Login to Vendor Dashboard](https://vendor.utahrealestate.com)

The retained material also uses the [vendor dashboard](https://vendor.utahrealestate.com/)
as its registration entry point; consult the provider for current onboarding.

## Authentication

The historical provider material discusses OAuth2/OpenID and vendor-issued bearer tokens. The Python wrapper accepts an already-issued bearer token; it does not implement an OAuth login, token exchange, or automatic refresh flow.

To access the API, simply pass your bearer token under the Authorization header:

`https://resoapi.utahrealestate.com/reso/odata`

```http
GET /reso/odata HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

Historical service-document response example (account access may differ):

```json
{
    "@odata.context": "https://resoapi.utahrealestate.com/reso/odata/$metadata",
    "value": [
        {
            "name": "Property",
            "url": "https://resoapi.utahrealestate.com/reso/odata/Property"
        },
        {
            "name": "Member",
            "url": "https://resoapi.utahrealestate.com/reso/odata/Member"
        },
        {
            "name": "Office",
            "url": "https://resoapi.utahrealestate.com/reso/odata/Office"
        },
        {
            "name": "OpenHouse",
            "url": "https://resoapi.utahrealestate.com/reso/odata/OpenHouse"
        },
        {
            "name": "Media",
            "url": "https://resoapi.utahrealestate.com/reso/odata/Media"
        },
        {
            "name": "DataSystem",
            "url": "https://resoapi.utahrealestate.com/reso/odata/DataSystem"
        },
        {
            "name": "Resource",
            "url": "https://resoapi.utahrealestate.com/reso/odata/Resource"
        },
        {
            "name": "PropertyGreenVerification",
            "url": "https://resoapi.utahrealestate.com/reso/odata/PropertyGreenVerification"
        },
        {
            "name": "PropertyUnitTypes",
            "url": "https://resoapi.utahrealestate.com/reso/odata/PropertyUnitTypes"
        },
        {
            "name": "HistoryTransactional",
            "url": "https://resoapi.utahrealestate.com/reso/odata/HistoryTransactional"
        },
        {
            "name": "Adu",
            "url": "https://resoapi.utahrealestate.com/reso/odata/Adu"
        },
        {
            "name": "Lookup",
            "url": "https://resoapi.utahrealestate.com/reso/odata/Lookup"
        }
    ]
}
```

See [OData endpoints](odata-endpoints.md) for service discovery, metadata, and resource paths, and the [Python authentication guide](../docs/getting-started/authentication.md) for the `bearer_token` constructor argument and environment variable. Resource names in the example do not imply that each has a main-client accessor; see [wrapper boundaries](index.md#protocol-and-wrapper-boundaries).
