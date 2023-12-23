from typer import Typer

from src.dusa_backend.scripts.populate_db import populate_db as _populate_database

app = Typer()


@app.command()
def populate_database():
    _populate_database()


@app.command()
def hello_world():
    print("Hello World!")


if __name__ == "__main__":
    app()
