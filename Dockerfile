FROM python:3.10-slim

WORKDIR /code


#COPY requirements.txt .
#RUN python -m pip install --upgrade pip
#RUN apt update; apt install -y git
#RUN pip install -r requirements.txt
#RUN apt remove -y git

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
#COPY run.py .

#COPY movies.db .
#COPY README.md .
#ENV NO_RATE_LIMIT="TRUE"
#ENV REDIS_HOST="redis"
#CMD uvicorn --host 0.0.0.0 --port 80 run:app --workers 4
