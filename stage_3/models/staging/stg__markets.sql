with markets as (
  SELECT * FROM {{ source("external_source", "NYC_Farmers_Markets") }}
)

SELECT DISTINCT
  "Market Name" as market_name,
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
  ST_Point(Latitude, Longitude) as point_geometry_wgs84,
  ST_Transform(point_geometry_wgs84, 'EPSG:4326', 'ESRI:102718') as geom,
FROM
  markets
