FROM pypy:3.8-slim-bullseye AS base
MAINTAINER Roberto Aguilar <r@rreboto.com>

RUN apt-get update && \
  apt-get install -q -y libpq5 && \
  pip install pipenv

# link pypy3 to python and python3 executables
RUN update-alternatives --install /usr/local/bin/python python /usr/local/bin/pypy3 100 && \
  update-alternatives --install /usr/local/bin/python3 python3 /usr/local/bin/pypy3 100

ENV SRC_DIR /usr/local/src/django-baseline
ENV APP_DIR ${SRC_DIR}/src

COPY Pipfile Pipfile.lock ${SRC_DIR}/

WORKDIR ${SRC_DIR}

RUN pipenv install --system --deploy --clear


FROM base AS builder

# install packages needed for builder
# as well as for CFFI version of psycopg2
RUN apt-get update && \
  apt-get install -q -y build-essential libssl-dev libpq-dev rsync && \
  pip install psycopg2cffi

WORKDIR ${SRC_DIR}

RUN pipenv install --system --deploy --dev --clear

RUN mkdir -p /var/lib/baseline
RUN rsync -a --include='gevent**' --include='psycopg2cffi**' --exclude='**' /opt/pypy/lib/pypy3.8/site-packages/ /var/lib/baseline/cffi_packages/


FROM base AS app

COPY --from=builder /var/lib/baseline/cffi_packages/ /opt/pypy/lib/pypy3.8/site-packages/

COPY files/ /
RUN chmod +x /usr/local/bin/*

COPY src/ ${APP_DIR}/

WORKDIR ${APP_DIR}

ARG VERSION

ENV VERSION=${VERSION}
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

CMD ["/usr/local/bin/run-gunicorn"]
