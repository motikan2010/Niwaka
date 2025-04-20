FROM python:3.12

COPY ./app /usr/app

WORKDIR /usr/app

RUN apt-get update \
  && apt -y install --no-install-recommends \
  && apt -y install git nodejs npm

RUN pip install uv \
  && pip install -r requirements.txt
