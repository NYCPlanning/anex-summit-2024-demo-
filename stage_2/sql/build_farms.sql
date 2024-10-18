LOAD spatial;
DROP TABLE IF EXISTS farms;
CREATE TABLE farms AS

WITH info AS (
  SELECT * FROM garden_info
),

block_lot AS (
  SELECT * FROM garden_block_lot
),

boroughs AS (
  SELECT * from cleaned__boroughs
),

all_garden_info AS (
  SELECT
    info.*,
    block_lot.* EXCLUDE (parksid),
  FROM
    info
  LEFT JOIN block_lot
    ON info.parksid = block_lot.parksid
),

garden_geometry AS (
  SELECT
    all_garden_info.*,
    -- ST_Point(all_garden_info.lon, all_garden_info.lat) as geom,
    ST_Transform(ST_Point(all_garden_info.lat, all_garden_info.lon), 'EPSG:4326', 'ESRI:102718') as geom,
  FROM
    all_garden_info
),

resolved_geometry AS (
  SELECT
    garden_geometry.* EXCLUDE (borough, geom),
    boroughs.boro_name as borough,
    (
      CASE
        WHEN boroughs.geom IS NOT NULL THEN true
        ELSE false
      END
    ) as geometry_is_in_nyc,
    (
      CASE
        WHEN geometry_is_in_nyc THEN garden_geometry.geom
        ELSE NULL
      END
    ) as geom,
  FROM
    garden_geometry
  LEFT JOIN boroughs
    ON ST_Intersects(garden_geometry.geom, boroughs.geom)
),

final AS (
  SELECT DISTINCT
    parksid,
    gardenname,
    juris as jurisdiction,
    borough,
    address,
    crossStreets as cross_streets,
    zipcode,
    BBL as bbl,
    lotsize,
    areacovered,
    status,
    openhrssu,
    openhrsm,
    openhrstu,
    openhrsw,
    openhrsth,
    openhrsf,
    openhrssa,
    coundist,
    communityboard,
    NTA as nta,
    CensusTract as census_tract,
    congressionaldist,
    assemblydist,
    statesenatedist,
    policeprecinct,
    lon as longitude,
    lat as latitude,
    ST_Transform(geom, 'ESRI:102718', 'EPSG:4326', always_xy := true) as point_geometry_wgs84,
  FROM
    resolved_geometry
  WHERE
    geometry_is_in_nyc
)

select * from final;