# Web API Documentation

## Overview

### Introduction

UtahRealEstate.com's web API (Application Programming Interface) is a RESO certified RESTful API built on OData v4.0. The API is both RESO web API Certified and RESO Data Dictionary Certified.

### What is a REST API?

REST stand for Representational State Transfer. This is an architectural pattern describing how distributed systems can expose a consistent interface. When the term is used, it generally refers to an API accessed via HTTP protocol at a predefined set of URLs.

These URLs represent various resources - any information or content accessed at that location, which can be returned as JSON, HTML, audio files, or images. Often, resources have one or more methods that can be performed on them over HTTP, like GET, POST, PUT and DELETE.

### Getting Started

Once you have registered for a data services account with UtahRealEstate.com, login into your account to view the status of your account, retrieve the bearer token, and accessible resources. This information can be found under Service Details.

[Login to Vendor Dashboard](https://vendor.utahrealestate.com)

If you are not registered with UtahRealEstate.com [click here to register](https://vendor.utahrealestate.com).

### Authentication

UtahRealEstate.com's web API supports OpenID and OAuth2 authorization/authentication protocols, and as part of previous web API certifications, is OpenID certified. Our API supports several grant types, however, we simplify the authentication process by providing a Bearer Token to our vendors.

To access the API, simply pass your bearer token under the Authorization header:

`https://resoapi.utahrealestate.com/reso/odata`

```http
GET /reso/odata HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

Response:

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

**https://resoapi.utahrealestate.com/reso/odata** is the Web API's Odata endpoint. See the next section, Odata Endpoints for more information on pulling data through resource endpoints. 