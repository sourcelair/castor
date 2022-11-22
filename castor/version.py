import tomllib


def get_poetry_version() -> str:
    with open("pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)
        return pyproject.get("tool", {}).get("poetry", {}).get("version", "n/a")
