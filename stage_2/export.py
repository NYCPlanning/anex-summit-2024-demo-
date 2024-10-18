from pathlib import Path
import duckdb

DATA_DIRECTORY = Path(__file__).parent.parent / "data"
DATABASE_PATH = DATA_DIRECTORY / "databases" / "stage_2.db"
OUTPUT_DATA_DIRECTORY = DATA_DIRECTORY / "output" / "stage_2"

TABLES_TO_EXPORT: list[str] = [
    "farms",
    "markets",
    "farm_to_market",
]


def _export_table(table_name: str, database: Path = DATABASE_PATH) -> None:
    print(f"Exporting table {table_name} ...")
    OUTPUT_DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

    with duckdb.connect(str(database)) as connection:
        connection.sql(
            f"COPY {table_name} TO '{OUTPUT_DATA_DIRECTORY / table_name}.csv' (HEADER, DELIMITER ',')"
        )
    with duckdb.connect(str(database)) as connection:
        connection.sql(
            f"COPY {table_name} TO '{OUTPUT_DATA_DIRECTORY / table_name}.parquet' (FORMAT PARQUET)"
        )
    with duckdb.connect(str(database)) as connection:
        connection.sql(f"LOAD spatial")
        connection.sql(
            f"COPY {table_name} TO '{OUTPUT_DATA_DIRECTORY / table_name}/' WITH (FORMAT GDAL, DRIVER 'ESRI Shapefile')"
        )


def export_tables() -> None:
    for table_name in TABLES_TO_EXPORT:
        _export_table(table_name)


if __name__ == "__main__":
    export_tables()
