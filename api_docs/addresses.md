# Provider Address Fields

This page preserves historical provider reference material. See the
[source and snapshot limitations](index.md#sources-and-snapshot-limits)
and [official provider documentation](https://docs.utahrealestate.com/).
Current account access and provider behavior have not been revalidated.

## Standard or grid address

The retained provider guidance uses a numeric `StreetName` with an empty
`StreetSuffix` as a heuristic for a grid address. Treat it as a formatting clue
and account for missing values; it is not a guaranteed validation rule for every
record.

## Standard addresses

The retained guide identifies these fields for a standard address:

- Street line: `StreetNumber` or `StreetNumberNumeric`, `StreetName`,
  `StreetSuffix`, and `UnitNumber`.
- Locality: `City`, `StateOrProvince`, `CountyOrParish`, and `PostalCode`.

Choose one street-number representation and account for missing optional parts
when formatting; do not append both numeric and string representations.

## Utah grid addresses

Utah grid addresses use two directional coordinates, such as `1300 E 9400 S`.
The retained provider material puts the numeric components in `StreetNumber`
and `CrossStreet`; `CrossStreet` represents the coordinate not represented by
`StreetNumber`.

The guide identifies these fields for a grid address:

- Street line: `StreetNumber`, `StreetDirPrefix`, `CrossStreet`, and
  `StreetDirSuffix`.
- Locality: `City`, `StateOrProvince`, `CountyOrParish`, and `PostalCode`.

These combinations are provider formatting guidance. The Python wrapper returns
provider fields and does not implement a canonical address formatter or address
geocoder. See the [property search guide](../docs/guides/property-search.md) for
implemented searches and [geolocation limitations](geolocation-search.md) before
assuming that an address query performs a spatial calculation.
