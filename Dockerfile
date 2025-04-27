FROM python:3.12-slim

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /breviori
COPY . .

RUN pip install --no-cache-dir poetry && \
    poetry config installer.max-workers 10 && \
    poetry install --no-interaction --no-ansi

EXPOSE 8080
ENTRYPOINT [ "./entrypoint.sh" ]

