FROM python:3.13-slim

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir poetry
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8080
CMD  poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080
