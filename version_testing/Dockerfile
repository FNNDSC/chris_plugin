# this Dockerfile is for the purposes of testing against different versions of Python.
# The source code should be mounted inside the container as a volume to
#     /usr/local/src/chris_plugin/chris_plugin

ARG  PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim
LABEL org.chrisproject.test=chris_plugin \
      org.chrisproject.python_version=${PYTHON_VERSION}

RUN pip install pytest

WORKDIR /usr/local/src/chris_plugin
COPY setup.py .

# Create shims for files which setup.py depend on.

RUN touch README.md && mkdir chris_plugin

RUN pip install -e .

CMD ["pytest", "--quiet"]
