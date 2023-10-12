import pytest

from chris_plugin.tool.image import ImageTag, InvalidTag


@pytest.mark.parametrize(
    "full_name, version, registry, user, name, repo, tag",
    [
        (
            "ghcr.io/fnndsc/pl-dcm2niix:1.2.3",
            "1.2.3",
            "ghcr.io",
            "fnndsc",
            "pl-dcm2niix",
            "fnndsc/pl-dcm2niix",
            "1.2.3",
        ),
        (
            "docker.io/fnndsc/pl-dcm2niix:1.2.3",
            "1.2.3",
            "docker.io",
            "fnndsc",
            "pl-dcm2niix",
            "fnndsc/pl-dcm2niix",
            "1.2.3",
        ),
        (
            "fnndsc/pl-dcm2niix:1.2.3",
            "1.2.3",
            "",
            "fnndsc",
            "pl-dcm2niix",
            "fnndsc/pl-dcm2niix",
            "1.2.3",
        ),
        (
            "fnndsc/pl-dcm2niix",
            "1.2.3",
            "",
            "fnndsc",
            "pl-dcm2niix",
            "fnndsc/pl-dcm2niix",
            "",
        ),
        (
            "quay.io/dne/something",
            "1.2.3",
            "quay.io",
            "dne",
            "something",
            "dne/something",
            "",
        ),
    ],
)
def test_parse_image_valid(full_name, version, registry, user, name, repo, tag):
    parsed = ImageTag(full_name, version, False)
    assert parsed.full_name == full_name
    assert parsed.registry == registry
    assert parsed.user == user
    assert parsed.name == name
    assert parsed.repo == repo
    assert parsed.tag == tag


@pytest.mark.parametrize(
    "example, version, msg",
    [
        (
            "docker.io/fnndsc/pl-civet@sha256:13726e3ae13b539e31ae2eecbbb0541e79f7fee8e7f485abf346c63c1055b484",
            "2.1.1",
            "Digest tags are not currently supported.",
        ),
        (
            "python:3",
            "3",
            f"python:3 is not a valid OCI image tag: must be in the form <registry>/<repo>/<name>:<version>",
        ),
        (
            "too/many/slashes/for/a/tag:5",
            "5",
            f"too/many/slashes/for/a/tag:5 is not a valid OCI image tag: must be in the form <registry>/<repo>/<name>:<version>",
        ),
    ],
)
def test_parse_image_invalid(example, version, msg):
    with pytest.raises(InvalidTag, match=msg):
        ImageTag(example, version)


@pytest.mark.parametrize(
    "example, version, msg",
    [
        (
            "ghcr.io/fnndsc/pl-helloworld",
            "4.3.2",
            "You should specify the image version in the tag, e.g. ghcr.io/fnndsc/pl-helloworld:4.3.2",
        ),
        (
            "ghcr.io/fnndsc/pl-helloworld:latest",
            "4.3.2",
            "You should specify the image version in the tag, e.g. ghcr.io/fnndsc/pl-helloworld:4.3.2",
        ),
        (
            "fnndsc/pl-helloworld:4.3.2",
            "4.3.2",
            "You should specify the registry, e.g. docker.io/fnndsc/pl-helloworld:4.3.2",
        ),
    ],
)
def test_warnings(example, version, msg, capsys):
    ImageTag(example, version)
    captured = capsys.readouterr()
    assert msg in captured.err
