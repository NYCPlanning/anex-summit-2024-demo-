WITH garden_info AS (
  SELECT * FROM {{ ref('stg__garden_info') }}
),

garden_block_lot AS (
  SELECT * FROM {{ ref('stg__garden_block_lot') }}
),

boroughs AS (
  SELECT * from {{ ref('stg__boroughs') }}
),

all_garden_details AS (
  SELECT
    garden_info.* EXCLUDE (gardenname),
    garden_info.gardenname as farm_name,
    garden_block_lot.* EXCLUDE (parksid),
  FROM
    garden_info
  LEFT JOIN garden_block_lot
    ON garden_info.parksid = garden_block_lot.parksid
),

garden_geometry AS (
  SELECT
    all_garden_details.*,
    ST_Transform(ST_Point(all_garden_details.latitude, all_garden_details.longitude), 'EPSG:4326', 'ESRI:102718') as geom,
  FROM
    all_garden_details
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
    ) as coordinates_in_nyc,
    (
      CASE
        WHEN coordinates_in_nyc THEN garden_geometry.geom
        ELSE NULL
      END
    ) as geom,
  FROM
    garden_geometry
  LEFT JOIN boroughs
    ON ST_Intersects(garden_geometry.geom, boroughs.geom)
)

select * from resolved_geometry