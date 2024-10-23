SELECT DISTINCT
  parksid,
  block,
  lotnum,
  lotsize,
  areacovered,
FROM
  {{ source("external_source", "GreenThumb_Block-Lot") }}
