---
link: https://www.geonames.org/export/
tags:
  - text
  - world
  - api
---

## Description

- Геолокации, атрибуты, населённые пункты, альтернативные названия.
## Examples


### GeoNames Webservice Credits

|Credits needed for a single web service call|   |
|---|---|
|postalCodeSearch|1 credit per request|
|findNearbyPostalCodes|2 credits per request, 3 credits for more than 500 records|
|search|1 credit per request|
|timezone|1 credit per request|
|findNearbyWikipedia|2 credits per request|
|wikipediaSearch|1 credit per request|
|findNearestAddress|1 credit per request|
|gtopo30|0.1 credit per request|
|srtm3|0.2 credit per request *|
|srtm1|0.3 credit per request *|
|astergdem|0.3 credit per request *|
|findNearByWeatherJSON|2 credits per request|
|findNearbyPlaceName|3 credits per request|
|rssToGeoRSS|4 per item in feed (for geocoding)  <br>0 if lat/lng are already included in feed|
|cities|4 credits per request|
|findNearby|4 credits per request|
|extendedFindNearby|4 credits per request|
|geonamesData.js|0.2 credit per request|

  
*: the elevation services srtm3 and astergdem allow to pass a list of lats/lngs. In this case the number of credits consumed depends on how much the cache can be used. Several identical or nearly identical lat/lng in the list will count as only one. The formula used is: Math .max( credits, credits * (10*elevationResult.elevationCredits.numDistinctTiles + elevationResult.elevationCredits.numDistinctPositions) / 10.0);

**All other web services need 1 credit per request.**
