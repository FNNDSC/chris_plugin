FROM docker.io/python:3.12.0-alpine3.18

WORKDIR /usr/local/src/simple_copy

COPY . .
RUN pip install .

CMD ["simple_copy", "--help"]
