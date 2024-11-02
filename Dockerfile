FROM python:3 AS base

ARG PROJECT_NAME=service-handler-api
RUN apt-get update
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
WORKDIR /app

ARG COMMIT
ENV COMMIT=$COMMIT

FROM base AS prod
ARG API_PORT
ENV API_PORT=$API_PORT
EXPOSE $API_PORT
ARG GUNICORN_RELOAD
ENV GUNICORN_RELOAD=$GUNICORN_RELOAD
ARG GUNICORN_WORKERS
ENV GUNICORN_WORKERS=$GUNICORN_WORKERS
ARG GUNICORN_WORKER_TIMEOUT
ENV GUNICORN_WORKER_TIMEOUT=$GUNICORN_WORKER_TIMEOUT
COPY src /app
CMD gunicorn -w $GUNICORN_WORKERS -c config.py -b 0.0.0.0:$API_PORT -t $GUNICORN_WORKER_TIMEOUT app $GUNICORN_RELOAD
