FROM docker.io/python:3.12.0-alpine3.18

WORKDIR /usr/local/src/replace

COPY . .
RUN pip install .

CMD ["replace", "--help"]
