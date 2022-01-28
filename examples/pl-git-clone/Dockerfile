FROM docker.io/python:3.10.2-alpine3.14

RUN apk add git

WORKDIR /usr/local/src/git_clone_wrapper

COPY . .
RUN pip install --use-feature=in-tree-build .

CMD ["git_clone_wrapper", "--help"]
