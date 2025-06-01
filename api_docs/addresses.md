# Addresses

## Addresses

### Standard or Grid

Standard addresses and grid addresses are formatted differently.  
If the StreetName is strictly numeric and the StreetSuffix is empty, it is most likely a grid address. Otherwise, it should be considered a standard address.

### Standard Addresses

The following RESO API fields can be used to build a standard address:   
StreetNumber/StreetNumberNumeric, StreetName, StreetSuffix, UnitNumber  
City, StateOrProvince, CountyOrParish, PostalCode  

### Grid Addresses

Street addresses in Utah are often based on a grid system. For example, 1300 E 9400 S. The numeric values for an address can be found in the RESO fields StreetNumber and CrossStreet.  
CrossStreet is mapped to either the North/South or East/West coordinate, whichever one is not represented in the StreetNumber.  

The following RESO API fields can be used to build a grid address:   
StreetNumber, StreetDirPrefix, CrossStreet, StreetDirSuffix  
City, StateOrProvince, CountyOrParish, PostalCode 