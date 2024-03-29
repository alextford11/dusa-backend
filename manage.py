from typer import Typer

from src.dusa_backend.scripts.populate_db import populate_db as _populate_database
from src.dusa_backend.scripts.remove_duplicate_stats import (
    remove_duplicate_health_stats as _remove_duplicate_health_stats,
)
from src.dusa_backend.scripts.remove_records import remove_records as _remove_records
from src.dusa_backend.scripts.atm_records_fix import atm_records_fix as _atm_records_fix
from src.dusa_backend.scripts.drinks_created_fix import (
    drinks_fix_matcher as _drinks_fix_matcher,
    change_drinks_created as _change_drinks_created,
)

app = Typer()


@app.command()
def populate_database():
    _populate_database()


@app.command()
def remove_duplicate_health_stats():
    _remove_duplicate_health_stats()


@app.command()
def remove_records():
    _remove_records()


@app.command()
def atm_records_fix():
    _atm_records_fix()


@app.command()
def drinks_fix_matcher():
    _drinks_fix_matcher()


@app.command()
def change_drinks_created():
    _change_drinks_created()


if __name__ == "__main__":
    app()
