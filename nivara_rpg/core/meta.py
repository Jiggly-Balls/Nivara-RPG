def get_version(pyproject_path: str = "pyproject.toml") -> None | str:
    """Reads the pyproject.toml file from the desired path and returns the version
    classifier if possible.

    Parameters
    ----------
    pyproject_path : str
        The path where the pyproject.toml file lies.
    """

    with open(pyproject_path, "r") as file:
        for line in file:
            if "version" in line:
                return line.split("=")[-1].strip().replace('"', "")
