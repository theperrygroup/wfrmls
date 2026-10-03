# Provider Geolocation Reference

This page records historical provider spatial syntax. See the
[source and snapshot limitations](index.md#sources-and-snapshot-limits) and the
[official provider documentation](https://docs.utahrealestate.com/) before
using it with a current vendor account.

## Python client behavior

`PropertyClient.search_properties_by_radius()` and
`PropertyClient.search_properties_by_polygon()` unconditionally raise
`ValidationError` before making an HTTP request. They cannot be used to execute
the historical queries below. This is a verified wrapper limitation; it does
not establish what a particular provider account currently supports.

For supported wrapper alternatives, see the
[geolocation guide](../docs/guides/geolocation.md) and
[property API reference](../docs/api/properties.md). City and address filters
can narrow results, but do not calculate a radius or polygon intersection.

## Historical radius expression

The retained material describes a query using `geo.distance` and a `GeoLocation`
field, centered at longitude `-111.898248`, latitude `40.576672`:

```text
geo.distance(GeoLocation,geography'SRID=3956;POINT(-111.898248 40.576672)') lt 1
```

The original page calls this a one-mile radius. The [schema snapshot](metadata.xml)
contains a `GeoLocation` field with `SRID=3956`, but its current availability and
the claimed distance unit have not been verified against current provider
documentation or an account schema. Do not treat the number `1` as a confirmed mile
conversion, or silently substitute a different coordinate system. Confirm the
available spatial field, coordinate reference system, and distance units with
the provider before constructing a query.

## Historical polygon expression

The retained example describes a polygon around part of Sandy using
longitude/latitude pairs. The first coordinate is repeated at the end to close
the polygon:

```text
geo.intersects(GeoLocation,geography'SRID=3956;POLYGON((-111.85518354177475 40.60508413156539,-111.85518354177475 40.55798337746534,-111.89896021038294 40.55798337746534,-111.89896021038294 40.60508413156539,-111.85518354177475 40.60508413156539))')
```

The same schema and coordinate-system limitations apply. These expressions are
retained for understanding older integrations, not offered as verified current
requests. See [query options](query-options.md) for nonspatial filtering and
[addresses](addresses.md) for Utah grid address conventions.
