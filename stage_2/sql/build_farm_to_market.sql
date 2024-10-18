LOAD spatial;
DROP TABLE IF EXISTS farm_to_market;
CREATE TABLE farm_to_market AS
SELECT
  farms.gardenname,
  farms.parksid,
  farms.latitude as garden_latitude,
  farms.longitude as garden_longitude,
  markets.name as market_name,
  markets.latitude as market_latitude,
  markets.longitude as market_longitude,
  cast(floor(
    ST_DISTANCE(
      ST_Transform(farms.point_geometry_wgs84, 'EPSG:4326', 'ESRI:102718', always_xy := true),
      ST_Transform(markets.point_geometry_wgs84, 'EPSG:4326', 'ESRI:102718', always_xy := true)
    )
  ) AS INTEGER) as distance_ft,
  ST_MakeLine(markets.point_geometry_wgs84, farms.point_geometry_wgs84) as line_geometry_wgs84,
FROM
  farms, markets
ORDER BY
  distance_ft ASC;