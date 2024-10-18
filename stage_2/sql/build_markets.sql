LOAD spatial;
DROP TABLE IF EXISTS markets;
CREATE TABLE markets AS

WITH boroughs AS (
  SELECT * from cleaned__boroughs
),

market_geometry AS (
  SELECT
    farmers_markets.*,
    -- ST_Point(farmers_markets.Longitude, farmers_markets.Latitude) as geom,
    ST_Transform(ST_Point(farmers_markets.Latitude, farmers_markets.Longitude), 'EPSG:4326', 'ESRI:102718') as geom,
  FROM
    farmers_markets
),

resolved_geometry AS (
  SELECT
    market_geometry.* EXCLUDE (borough, geom),
    boroughs.boro_name as borough,
    (
      CASE
        WHEN boroughs.geom IS NOT NULL THEN true
        ELSE false
      END
    ) as geometry_is_in_nyc,
    (
      CASE
        WHEN geometry_is_in_nyc THEN market_geometry.geom
        ELSE NULL
      END
    ) as geom,
  FROM
    market_geometry
  LEFT JOIN boroughs
    ON ST_Intersects(market_geometry.geom, boroughs.geom)
),

final AS (
  SELECT DISTINCT
    "Market Name" as name,
    "Accepts EBT" as accepts_ebt,
    "Distributes Health Bucks?" as distributes_health_bucks,
    (
      CASE
        WHEN "Open Year-Round" = 'Yes' THEN true
        WHEN "Open Year-Round" = 'No' THEN false
        ELSE NULL
      END
    ) as open_year_round,
    "Street Address" as address,
    "Borough" as borough,
    "Latitude" as latitude,
    "Longitude" as longitude,
    ST_Transform(geom, 'ESRI:102718', 'EPSG:4326', always_xy := true) as point_geometry_wgs84,
  FROM
    resolved_geometry
  WHERE
    geometry_is_in_nyc
)

select * from final;