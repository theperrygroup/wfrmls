#!/usr/bin/env python3
from wfrmls import WFRMLSClient
import json

# Configure WFRMLS_BEARER_TOKEN in the environment or an ignored local .env file.
client = WFRMLSClient()

print("Searching for property with ListingId: 2089701")

# Try filter query approach
properties = client.property.get_properties(filter_query="ListingId eq '2089701'")

print(f"Found {len(properties['value'])} properties")

if properties["value"]:
    print("\nProperty Data:")
    print(json.dumps(properties["value"][0], indent=2))
else:
    print("No property found with that ListingId")
