#!/bin/bash

cd /app/database && alembic upgrade head && cd /app

uvicorn main:app --host 0.0.0.0 --port ${FASTAPI_PORT} --reload
