# Change Log

## Change Log

| Type    | Date       | Description                                                                                                                                             |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Update  | 2020-11-06 | Removed all underscores from lookup enum text. So for example Single\_Family\_Residence would now be SingleFamilyResidence                              |
| Update  | 2020-11-09 | ResourceRecordKey and ResourceRecordID in the Media resource are now Strings instead of Integers                                                        |
| Release | 2020-11-18 | Added option to receive non-annotated enumerations in the payload.                                                                                      |
| Bug Fix | 2020-11-25 | The values for VirtualTourURLBranded and VirtualTourURLUnbranded were reversed. This has been resolved.                                                 |
| Bug Fix | 2020-12-01 | Fixed incorrect lookup values for: PatioAndPorchFeatures, View, Sewer, OtherEquipment, FireplaceFeatures and DoorFeatures                               |
| Update  | 2021-02-23 | Each resources now has a proper OriginatingSystemKey. This field is a hash that can be used as a unique record identifier, from the Originating system. |
| Release | 2021-03-25 | Released HistoryTransactional resource. This resource has historical changelog data for property listings.                                              |
| Release | 2021-04-12 | Added field ImageStatus. This is a flag type of field that will let the vendor know if at least on image related to the listing is private.             |
| Release | 2021-04-12 | Added field CancellationDate. This is a date field indicating when a listing was canceled.                                                              | 