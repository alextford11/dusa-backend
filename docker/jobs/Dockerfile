FROM python:3.11

WORKDIR /code

COPY ../../pyproject.toml /code/pyproject.toml
COPY ../../src /code/src

RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
