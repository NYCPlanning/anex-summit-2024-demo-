from pathlib import Path
import duckdb

DATA_DIRECTORY = Path(__file__).parent.parent / "data"
DATABASE_PATH = DATA_DIRECTORY / "databases" / "stage_2.db"
SOURCE_DATA_DIRECTORY = DATA_DIRECTORY / "source_data"
SQL_DIRECTORY = Path(__file__).parent / "sql"


def _run_sql_file(filepath: Path, database: Path = DATABASE_PATH) -> None:
    print(f"Running sql file {filepath} ...")

    with open(filepath) as query_file:
        query = query_file.read()

    with duckdb.connect(str(database)) as connection:
        result = connection.sql(query)
        if result:
            result.show()


def run_some_files() -> None:
    _run_sql_file(SQL_DIRECTORY / "build_boroughs.sql")
    _run_sql_file(SQL_DIRECTORY / "build_markets.sql")
    _run_sql_file(SQL_DIRECTORY / "build_farms.sql")
    _run_sql_file(SQL_DIRECTORY / "build_farm_to_market.sql")


if __name__ == "__main__":
    run_some_files()
