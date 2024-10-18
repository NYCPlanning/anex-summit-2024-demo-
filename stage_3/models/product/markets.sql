{{ config(materialized='external', location='../data/output/stage_3/market_name.csv') }}
{{ config(materialized='external', location='../data/output/stage_3/market_name.parquet') }}
SELECT
  market_name
FROM {{ ref('stg__markets') }}
