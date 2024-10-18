{{ config(materialized='external', location='../data/output/stage_3/farms.csv') }}
{{ config(materialized='external', location='../data/output/stage_3/farms.parquet') }}
SELECT
  farm_name
FROM {{ ref('int__farms') }}
