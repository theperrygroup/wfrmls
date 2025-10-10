#!/usr/bin/env python3
from wfrmls import WFRMLSClient
import json

client = WFRMLSClient(bearer_token="9d0243d7632d115b002acf3547d2d7ee")

print("Searching for property with ListingId: 2089701")

# Try filter query approach
properties = client.property.get_properties(
    filter_query="ListingId eq '2089701'"
)

print(f"Found {len(properties['value'])} properties")

if properties['value']:
    print("\nProperty Data:")
    print(json.dumps(properties['value'][0], indent=2))
else:
    print("No property found with that ListingId") 