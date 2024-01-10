FROM python:3.11

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml
COPY ./entrypoint.sh /code/entrypoint.sh
COPY ./alembic.ini /code/alembic.ini
COPY ./src /code/src

RUN chmod +x entrypoint.sh

RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

EXPOSE 8000

CMD ["/code/entrypoint.sh"]
