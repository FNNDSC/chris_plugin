# Python Version Testing

On Github Actions, testing across versions of Python is achieved
with a build matrix.
See [../.github/workflows/test.yml](../.github/workflows/test.yml).

In this directory is an over-engineered solution to run those tests using Docker.

## Usage

```shell
make build
make test
make clean
```
