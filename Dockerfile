FROM python:3.12-slim AS base
RUN apt-get update && apt-get install -y --no-install-recommends gcc g++ build-essential libpq-dev && apt-get clean
RUN pip install --no-cache-dir --upgrade pip
WORKDIR /home/app

FROM base AS packages
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

FROM packages AS app
COPY . .
CMD ["fastapi", "dev", "src/infrastructure/ports/api/main.py", "--host", "0.0.0.0", "--port", "80"]