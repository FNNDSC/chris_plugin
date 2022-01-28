FROM docker.io/python:3.10.2-alpine3.14

WORKDIR /usr/local/src/replace

COPY . .
RUN pip install --use-feature=in-tree-build .

CMD ["replace", "--help"]
