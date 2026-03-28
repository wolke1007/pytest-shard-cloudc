import nox

nox.options.default_venv_backend = "none"
nox.options.sessions = ["tests", "shard-0", "shard-1", "lint", "typing"]


@nox.session(name="tests", python=False)
def tests(session: nox.Session) -> None:
    session.run("python", "-m", "pytest", "tests", external=True)


@nox.session(name="shard-0", python=False)
def shard_zero(session: nox.Session) -> None:
    session.run(
        "python",
        "-m",
        "pytest",
        "--shard-id=0",
        "--num-shards=2",
        "tests",
        external=True,
    )


@nox.session(name="shard-1", python=False)
def shard_one(session: nox.Session) -> None:
    session.run(
        "python",
        "-m",
        "pytest",
        "--shard-id=1",
        "--num-shards=2",
        "tests",
        external=True,
    )


@nox.session(name="lint", python=False)
def lint(session: nox.Session) -> None:
    session.run("python", "-m", "ruff", "check", "pytest_shard", "tests", external=True)
    session.run(
        "python",
        "-m",
        "ruff",
        "format",
        "--check",
        "pytest_shard",
        "tests",
        external=True,
    )


@nox.session(name="typing", python=False)
def typing(session: nox.Session) -> None:
    session.run("python", "-m", "mypy", "pytest_shard", external=True)
