import sys


class InvalidTag(Exception):
    pass


class ImageTag:
    def __init__(self, tag: str, version: str, warnings=True):
        if "@" in tag:
            raise InvalidTag("Digest tags are not currently supported.")
        if len(split_on_colon := tag.split(":", maxsplit=1)) == 2:
            before_colon, after_colon = split_on_colon
        else:
            before_colon = tag
            after_colon = ""

        if warnings and version not in after_colon:
            _warn(
                f"You should specify the image version in the tag, e.g. {before_colon}:{version}"
            )

        parts = before_colon.split("/")
        if len(parts) == 2:
            if warnings:
                _warn(f"You should specify the registry, e.g. docker.io/{tag}")
            registry = ""
            user, name = parts
        elif len(parts) == 3:
            registry, user, name = parts
        else:
            raise InvalidTag(
                f"{tag} is not a valid OCI image tag: must be in the form <registry>/<repo>/<name>:<version>"
            )

        self.full_name = tag
        self.registry = registry
        self.user = user
        self.name = name
        self.repo = f"{user}/{name}"
        self.tag = after_colon


def _warn(msg: str):
    print("\033[1;33mWARNING\033[22;39m", end=": ", file=sys.stderr)
    print(msg, file=sys.stderr)
