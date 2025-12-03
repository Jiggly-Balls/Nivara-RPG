FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.9.15 /uv /uvx /bin/

ADD nivara_rpg/ nivara_rpg/
ADD .env .
ADD uv.lock .
ADD pyproject.toml .

RUN uv sync --locked --no-install-project --no-dev

CMD ["uv", "run", "--no-dev", "./nivara_rpg/main.py"]