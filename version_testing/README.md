# Python Version Testing

In this directory is an over-engineered solution to run unit tests in Docker on a local machine.

On Github Actions, testing across versions of Python is achieved
using a build matrix instead.
See [../.github/workflows/test.yml](../.github/workflows/test.yml).

## Usage

```shell
make build
make test
make clean
```
