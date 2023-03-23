FROM --platform=linux/amd64 python:3.8-slim-bullseye AS base
MAINTAINER Roberto Aguilar <r@rreboto.com>

RUN apt-get update \
  && apt-get install -q -y libpq5 \
  && pip install pipenv

RUN pip install psycopg2-binary

ENV SRC_DIR /usr/local/src/django-baseline
ENV APP_DIR ${SRC_DIR}/src

COPY Pipfile Pipfile.lock ${SRC_DIR}/

WORKDIR ${SRC_DIR}

RUN pipenv install --system --deploy --clear

COPY files/ /
RUN chmod +x /usr/local/bin/*

FROM base AS builder

RUN pipenv install --system --deploy --dev --clear

COPY src/ ${APP_DIR}/

WORKDIR ${APP_DIR}

RUN DJANGO_SETTINGS_MODULE=bltestproject.settings ./manage.py collectstatic --no-input

ARG VERSION

ENV VERSION=${VERSION}
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

CMD ["/usr/local/bin/run-pytest"]


FROM base AS app

COPY --from=builder ${APP_DIR} ${APP_DIR}

WORKDIR ${APP_DIR}

ARG VERSION

ENV VERSION=${VERSION}
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

CMD ["/usr/local/bin/run-gunicorn"]
