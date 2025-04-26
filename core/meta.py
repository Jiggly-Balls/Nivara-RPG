def get_version(pyproject_path: str = "pyproject.toml") -> None | str:
    with open(pyproject_path, "r") as file:
        for line in file:
            if "version" in line:
                return line.split("=")[-1].strip()
