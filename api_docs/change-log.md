# Change Log

This page preserves historical provider reference material. See the
[source and snapshot limitations](index.md#sources-and-snapshot-limits)
and [official provider documentation](https://docs.utahrealestate.com/).
Current account access and provider behavior have not been revalidated.

This is the retained **provider** change log, ending April 12, 2021. It is not
the Python package release history and does not claim that the provider has had
no later changes. For wrapper releases, see the
[repository releases](https://github.com/theperrygroup/wfrmls/releases).

| Type    | Date       | Description                                                                                                                                             |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Update  | 2020-11-06 | Removed all underscores from lookup enum text. So for example Single\_Family\_Residence would now be SingleFamilyResidence                              |
| Update  | 2020-11-09 | ResourceRecordKey and ResourceRecordID in the Media resource are now Strings instead of Integers                                                        |
| Release | 2020-11-18 | Added option to receive non-annotated enumerations in the payload.                                                                                      |
| Bug Fix | 2020-11-25 | The values for VirtualTourURLBranded and VirtualTourURLUnbranded were reversed. This has been resolved.                                                 |
| Bug Fix | 2020-12-01 | Fixed incorrect lookup values for: PatioAndPorchFeatures, View, Sewer, OtherEquipment, FireplaceFeatures and DoorFeatures                               |
| Update  | 2021-02-23 | Each resource now has a proper OriginatingSystemKey. This field is a hash that can be used as a unique record identifier, from the Originating system. |
| Release | 2021-03-25 | Released HistoryTransactional resource. This resource has historical changelog data for property listings.                                              |
| Release | 2021-04-12 | Added field ImageStatus. This is a flag type of field that will let the vendor know if at least one image related to the listing is private.             |
| Release | 2021-04-12 | Added field CancellationDate. This is a date field indicating when a listing was canceled.                                                              |
