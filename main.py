import dotenv

ENV = dotenv.dotenv_values(".env")
TOKEN = ENV["TOKEN"]

if TOKEN is None:
    raise RuntimeError("No token was provided in the .env file.")


async def main() -> None: ...
