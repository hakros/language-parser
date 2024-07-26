FROM python:3.11-bookworm
WORKDIR /app
COPY . .
RUN apt-get update
RUN pip install -r ./requirements.txt