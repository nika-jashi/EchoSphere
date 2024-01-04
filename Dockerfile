FROM python:3.10.11-slim-buster

LABEL maintainer="nikajashi"

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/requirements.txt
COPY . /app

WORKDIR /app
EXPOSE 8000

ARG DEV=false

RUN python -m venv /py && /py/bin/pip install --upgrade pip && /py/bin/pip install -r /tmp/requirements.txt && rm -rf /tmp


ENV PATH="/py/bin:$PATH"

USER root

RUN chmod +x /app/scripts/docker-entrypoint.sh
RUN chmod +x ../py/bin/activate

ENTRYPOINT ["/app/scripts/docker-entrypoint.sh"]