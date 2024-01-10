#!/bin/sh

alembic upgrade head
uvicorn src.dusa_backend.main:app --host 0.0.0.0 --port 8000
