# Web API OData Endpoints

## OData Endpoints

UtahRealEstate.com's web API is built on OData v4.0. Web API resources can be queried through the OData endpoints accessible to the vendor.

### Service Document

The web API exposes two endpoints that a vendor can use to get information about the resources and fields available to them.

The OData Service Document endpoint shows all resources that are available to the vendor.

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
        }
    ]
}
```

### Metadata

The OData Metadata endpoint shows all resources, fields, enumerations and entity relationships available to the vendor.

`https://resoapi.utahrealestate.com/reso/odata/$metadata`

```http
GET /reso/odata/$metadata HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

Response:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<edmx:Edmx xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx" Version="4.0">
    <edmx:DataServices>
        <Schema xmlns="http://docs.oasis-open.org/odata/ns/edm" Namespace="Default">
            <EntityContainer Name="Container">
                <EntitySet EntityType="Odata.Models.Property" Name="Property">
                    <NavigationPropertyBinding Path="Media" Target="Media"/>
                    <NavigationPropertyBinding Path="Member" Target="Member"/>
                    <NavigationPropertyBinding Path="Office" Target="Office"/>
                    <NavigationPropertyBinding Path="OpenHouse" Target="OpenHouse"/>
                    <NavigationPropertyBinding Path="PropertyGreenVerification" Target="PropertyGreenVerification"/>
                    <NavigationPropertyBinding Path="PropertyUnitTypes" Target="PropertyUnitTypes"/>
                </EntitySet>
                <EntitySet EntityType="Odata.Models.Member" Name="Member">
                    <NavigationPropertyBinding Path="Property" Target="Property"/>
                    <NavigationPropertyBinding Path="Office" Target="Office"/>
                </EntitySet>
                <EntitySet EntityType="Odata.Models.Office" Name="Office">
                    <NavigationPropertyBinding Path="Property" Target="Property"/>
                    <NavigationPropertyBinding Path="Member" Target="Member"/>
                </EntitySet>
                <EntitySet EntityType="Odata.Models.OpenHouse" Name="OpenHouse">
                    <NavigationPropertyBinding Path="Property" Target="Property"/>
                </EntitySet>
                <EntitySet EntityType="Odata.Models.Media" Name="Media">
                    <NavigationPropertyBinding Path="Property" Target="Property"/>
                </EntitySet>
                <EntitySet EntityType="Odata.Models.DataSystem" Name="DataSystem"/>
                <EntitySet EntityType="Odata.Models.Resource" Name="Resource"/>
                <EntitySet EntityType="Odata.Models.PropertyGreenVerification" Name="PropertyGreenVerification"/>
                <EntitySet EntityType="Odata.Models.PropertyUnitTypes" Name="PropertyUnitTypes"/>
            </EntityContainer>
        </Schema>

        ..........

        <EnumType IsFlags="false" Name="StandardStatus" UnderlyingType="Edm.Int32">
            <Member Name="Active" Value="1"/>
            <Member Name="Pending" Value="7"/>
            <Member Name="Withdrawn" Value="3"/>
            <Member Name="Expired" Value="5"/>
            <Member Name="ActiveUnderContract" Value="2">
                <Annotation String="Active Under Contract" Term="RESO.OData.Metadata.StandardName"/>
            </Member>
            <Member Name="Closed" Value="6"/>
            <Member Name="Canceled" Value="4"/>
        </EnumType>

        ..........

        <EntityType Name="Property">
            <Key>
                <PropertyRef Name="ListingKeyNumeric"/>
            </Key>
            <Property Name="ListingKeyNumeric" Precision="255" Scale="0" Type="Edm.Int32"/>
            <Property Name="AssociationFee" Precision="14" Scale="2" Type="Edm.Decimal"/>
            <Property Name="RoomsTotal" Precision="3" Scale="0" Type="Edm.Int32"/>
            <Property Name="Stories" Precision="2" Scale="0" Type="Edm.Int32"/>
            <Property Name="BathroomsFull" Precision="3" Scale="0" Type="Edm.Int32"/>

        ..........
```

### Resource Endpoints

The web API will expose an endpoint for each resource available to the vendor. Each of these endpoints can be searched, filtered and sorted using OData's system query options.

* https://resoapi.utahrealestate.com/reso/odata/Property
* https://resoapi.utahrealestate.com/reso/odata/Member
* https://resoapi.utahrealestate.com/reso/odata/Office
* https://resoapi.utahrealestate.com/reso/odata/OpenHouse
* https://resoapi.utahrealestate.com/reso/odata/Media
* https://resoapi.utahrealestate.com/reso/odata/PropertyGreenVerification
* https://resoapi.utahrealestate.com/reso/odata/PropertyUnitTypes
* https://resoapi.utahrealestate.com/reso/odata/HistoryTransactional

To get the most recent data from an endpoint, use the query option **$orderby** and the **ModificationTimestamp** field in descending order.

For example, to get the most recent listings query the Property resource.

`https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ModificationTimestamp desc`

```http
GET /reso/odata/Property?$orderby=ModificationTimestamp%20desc HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

```json
{
    "@odata.context": "$metadata#Property",
    "value": [
        {
            "@odata.id": "Property(1611952)",
            "ListingKeyNumeric": 1611952,
            "RoomsTotal": 17,
            "ListPrice": 2950000.0,
            "ModificationTimestamp": "2019-10-03T10:04:24Z"
            .........
```

Note: white spaces need to be encoded as %20 if your client does not do it for you. For example $orderby=ModificationTimestamp%20desc

See the next section, OData Query Options for examples of pulling, filtering, and sorting data. 