FROM python:3.11

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml
COPY ./src /code/src

RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

EXPOSE 8000

CMD ["uvicorn", "src.dusa_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
