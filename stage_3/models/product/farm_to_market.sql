{{ config(materialized='external', location='../data/output/stage_3/farm_to_market.csv') }}
{{ config(materialized='external', location='../data/output/stage_3/farm_to_market.parquet') }}

WITH markets as (SELECT * FROM {{ ref('stg__markets') }}),

farms as (SELECT * FROM {{ ref('int__farms') }}),

nyc_markets as (
  SELECT DISTINCT
    market_name,
    coordinates_in_nyc,
    point_geometry_wgs84,
  FROM markets
  WHERE coordinates_in_nyc
),

nyc_farms as (
  SELECT DISTINCT
    farm_name,
    coordinates_in_nyc,
    point_geometry_wgs84,
  FROM farms
  WHERE coordinates_in_nyc
),

combined as (
  SELECT
    nyc_markets.market_name as market_name,
    nyc_farms.farm_name,
    cast(floor(
      ST_DISTANCE(
        ST_Transform(nyc_markets.point_geometry_wgs84, 'EPSG:4326', 'ESRI:102718', always_xy := true),
        ST_Transform(nyc_farms.point_geometry_wgs84, 'EPSG:4326', 'ESRI:102718', always_xy := true)
      )
    ) AS INTEGER) as distance_ft,
    ST_MakeLine(nyc_markets.point_geometry_wgs84, nyc_farms.point_geometry_wgs84) as line_geometry_wgs84,
  FROM
    nyc_farms, nyc_markets
)

select * from combined
ORDER BY
  distance_ft ASC
