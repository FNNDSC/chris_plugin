FROM docker.io/python:3.12.0-alpine3.18

RUN apk add git

WORKDIR /usr/local/src/git_clone_wrapper

COPY . .
RUN pip install .

CMD ["git_clone_wrapper", "--help"]
