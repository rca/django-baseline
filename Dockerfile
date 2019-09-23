FROM python:3.7-slim-buster
MAINTAINER Roberto Aguilar <r@rreboto.com>

RUN pip install pipenv

ENV SRC_DIR /usr/local/src/django-baseline
ENV APP_DIR ${SRC_DIR}/src

COPY Pipfile Pipfile.lock ${SRC_DIR}/

WORKDIR ${SRC_DIR}

RUN pipenv install --system --deploy --clear


COPY files/ /
RUN chmod +x /usr/local/bin/*

COPY src/ ${APP_DIR}/

WORKDIR ${APP_DIR}

ARG VERSION

ENV BASELINE_VERSION=${VERSION}
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

CMD ["/usr/local/bin/run-gunicorn"]
