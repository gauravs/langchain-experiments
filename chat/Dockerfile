FROM python:3.11.7-bookworm

RUN pip install poetry==1.5.1

COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry config virtualenvs.create false && \
    poetry install \
      --no-interaction \
      --no-ansi \
      --no-root \
      --no-directory
