from pathlib import Path
import duckdb
from dataclasses import dataclass

DATA_DIRECTORY = Path(__file__).parent.parent / "data"
DATABASE_PATH = DATA_DIRECTORY / "stage_2.db"
SOURCE_DATA_DIRECTORY = DATA_DIRECTORY / "source_data"


@dataclass
class SourceDataset:
    table_name: str
    file_path: Path
    is_spatial: bool = False


source_datasets = [
    SourceDataset(
        table_name="borough_boundaries",
        file_path=SOURCE_DATA_DIRECTORY / "Borough Boundaries.geojson",
        is_spatial=True,
    ),
    SourceDataset(
        table_name="farmers_markets",
        file_path=SOURCE_DATA_DIRECTORY / "NYC_Farmers_Markets.csv",
    ),
    SourceDataset(
        table_name="garden_info",
        file_path=SOURCE_DATA_DIRECTORY / "GreenThumb_Garden_Info.csv",
    ),
    SourceDataset(
        table_name="garden_block_lot",
        file_path=SOURCE_DATA_DIRECTORY / "GreenThumb_Block-Lot.csv",
    ),
]


def _db_connection():
    connection = duckdb.connect(str(DATABASE_PATH))
    connection.sql(f"LOAD spatial;")
    return connection


def create_database():
    # delete the database if it exists
    DATABASE_PATH.unlink(missing_ok=True)
    # create the database
    connection = _db_connection()
    with _db_connection() as connection:
        connection.sql(f"INSTALL spatial;")
    print(f"✅ Created a persistent database at: {DATABASE_PATH}")
    return connection


def load_source_data():
    for dateset in source_datasets:
        print(f"Loading source dataset {dateset}")
        if dateset.is_spatial:
            with _db_connection() as connection:
                connection.sql(
                    f"CREATE TABLE {dateset.table_name} as SELECT * FROM ST_Read('{dateset.file_path}')"
                )
                connection.sql(f"DESCRIBE TABLE {dateset.table_name}").show()
        else:
            with _db_connection() as connection:
                connection.sql(f"DESCRIBE TABLE '{dateset.file_path}'").show()
                connection.sql(
                    f"CREATE TABLE {dateset.table_name} as SELECT * FROM '{dateset.file_path}'"
                )
        print(f"✅ Loaded source dataset {dateset.table_name}")
    
    with _db_connection() as connection:
        connection.sql(f"SHOW ALL TABLES").show()
    print(f"✅ Loaded all source data to database {DATABASE_PATH}")


if __name__ == "__main__":
    create_database()
    load_source_data()
