import os
from pathlib import Path
import duckdb

DATA_DIRECTORY = Path(__file__).parent.parent / "data"
DATABASE_PATH = DATA_DIRECTORY / "stage_1.db"
SOURCE_DATA_DIRECTORY = DATA_DIRECTORY / "source_data"
HTTP_PROXY = os.environ["http_proxy"]


def create_database():
    # delete the database if it exists
    DATABASE_PATH.unlink(missing_ok=True)
    # create the database
    connection = duckdb.connect(str(DATABASE_PATH))
    # install the spatial extension
    with duckdb.connect(str(DATABASE_PATH)) as connection:
        connection.sql(f"SET http_proxy TO '{HTTP_PROXY}'")
        connection.sql(f"INSTALL spatial")
        connection.sql(f"LOAD spatial")
    print(f"✅ Created a persistent database at: {DATABASE_PATH}")
    return connection


def load_pluto():
    pluto_csv_path = SOURCE_DATA_DIRECTORY / "pluto.csv"
    print("Creating PLUTO table from local csv ...")
    with duckdb.connect(str(DATABASE_PATH)) as connection:
        connection.sql(f"DESCRIBE TABLE '{pluto_csv_path}'").show()
        connection.sql(f"CREATE TABLE pluto as SELECT * FROM '{pluto_csv_path}'")
        connection.sql("SHOW ALL TABLES").show()

    print("✅ Loaded PLUTO data")


def load_airbnb():
    airbnb_nyc_listings_url = "https://data.insideairbnb.com/united-states/ny/new-york-city/2024-07-05/visualisations/listings.csv"
    airbnb_nyc_detailed_listings_url = "https://data.insideairbnb.com/united-states/ny/new-york-city/2024-07-05/data/listings.csv.gz"
    print("Creating Airbnb NYC listings table from remote csv file ...")
    with duckdb.connect(str(DATABASE_PATH)) as connection:
        connection.sql(f"SET http_proxy TO '{HTTP_PROXY}'")
        connection.sql(f"DESCRIBE TABLE '{airbnb_nyc_listings_url}'").show()
        connection.sql(
            f"CREATE TABLE airbnb_nyc_listings as SELECT * FROM '{airbnb_nyc_listings_url}'"
        )
    print(
        "Creating Airbnb NYC detailed listings table from remote compressed csv file ..."
    )
    with duckdb.connect(str(DATABASE_PATH)) as connection:
        connection.sql(f"SET http_proxy TO '{HTTP_PROXY}'")
        connection.sql(f"DESCRIBE TABLE '{airbnb_nyc_detailed_listings_url}'").show()
        connection.sql(
            f"CREATE TABLE airbnb_nyc_detailed_listings as SELECT * FROM '{airbnb_nyc_detailed_listings_url}'"
        )
        connection.sql("SHOW ALL TABLES").show()

    print("✅ Loaded Airbnb data")


def load_taxi():
    yellow_cab_trips_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
    green_cab_trips_url = (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2024-01.parquet"
    )
    for_hire_trips_url = (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2024-01.parquet"
    )
    high_volume_for_hire_trips_url = (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_2024-01.parquet"
    )
    tlc_trip_urls = [
        yellow_cab_trips_url,
        green_cab_trips_url,
        for_hire_trips_url,
        high_volume_for_hire_trips_url,
    ]
    print("Creating Taxi tables from remote parquet files ...")
    with duckdb.connect(str(DATABASE_PATH)) as connection:
        connection.sql(f"SET http_proxy TO '{HTTP_PROXY}'")
        for remote_table in tlc_trip_urls:
            connection.sql(f"DESCRIBE TABLE '{remote_table}'").show()
        connection.sql(
            f"CREATE TABLE tlc_trips as SELECT * FROM read_parquet({tlc_trip_urls}, union_by_name = true, filename = true)"
        )
        connection.sql("SHOW ALL TABLES").show()
    print("✅ Loaded Taxi data")


if __name__ == "__main__":
    create_database()
    load_pluto()
    load_airbnb()
    load_taxi()
