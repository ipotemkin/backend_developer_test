FROM python:3.10-slim

WORKDIR /code

RUN apt update \
    && apt install -y \
#     --no-install-recommends \
#    postgresql \
    gcc \
#    python3-dev \
#    musl-dev \
    libpq-dev \
    && apt autoclean && apt autoremove \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* /var/tmp/*

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code
