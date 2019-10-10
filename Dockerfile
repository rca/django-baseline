FROM pypy:3.6-slim-stretch
MAINTAINER Roberto Aguilar <r@rreboto.com>

RUN apt-get update && \
  apt-get install -q -y build-essential libssl-dev libpq-dev && \
  pip install pipenv psycopg2cffi

# link pypy3 to python and python3 executables
RUN update-alternatives --install /usr/local/bin/python python /usr/local/bin/pypy3 100 && \
  update-alternatives --install /usr/local/bin/python3 python3 /usr/local/bin/pypy3 100

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

ENV VERSION=${VERSION}
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

CMD ["/usr/local/bin/run-gunicorn"]