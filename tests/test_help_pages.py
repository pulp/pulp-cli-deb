import typing as t

import click
import pytest
from click.testing import CliRunner
from packaging.version import parse as parse_version
from pulp_cli import __version__ as PULP_CLI_VERSION
from pulp_cli import load_plugins, main

load_plugins()


def traverse_commands(command: click.Command, args: t.List[str]) -> t.Iterator[t.List[str]]:
    yield args

    if isinstance(command, click.Group):
        for name, sub in command.commands.items():
            yield from traverse_commands(sub, args + [name])

        params = command.params
        if params:
            if "--type" in params[0].opts:
                # iterate over commands with specific context types
                assert isinstance(params[0].type, click.Choice)
                for context_type in params[0].type.choices:
                    yield args + ["--type", context_type]

                    for name, sub in command.commands.items():
                        yield from traverse_commands(sub, args + ["--type", context_type, name])


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    m = next(metafunc.definition.iter_markers("help_page"), None)
    if m is not None and "base_cmd" in m.kwargs:
        if parse_version(PULP_CLI_VERSION) < parse_version("0.24"):
            pytest.skip("This test is incompatible with older cli versions.")
        rel_main: click.Group = main
        base_cmd = m.kwargs["base_cmd"]
        for step in base_cmd:
            sub = rel_main.commands[step]
            assert isinstance(sub, click.Group)
            rel_main = sub
        metafunc.parametrize("args", traverse_commands(rel_main, base_cmd), ids=" ".join)


@pytest.fixture
def no_api(monkeypatch: pytest.MonkeyPatch) -> None:
    @property  # type: ignore
    def getter(self: t.Any) -> None:
        pytest.fail("Invalid access to 'PulpContext.api'.", pytrace=False)

    monkeypatch.setattr("pulp_glue.common.context.PulpContext.api", getter)


@pytest.mark.help_page(base_cmd=["deb"])
def test_accessing_the_help_page_does_not_invoke_api(
    no_api: None,
    args: list[str],
) -> None:
    runner = CliRunner()
    result = runner.invoke(main, args + ["--help"], catch_exceptions=False)

    if result.exit_code == 2:
        assert (
            "not available in this context" in result.stdout
            or "not available in this context" in result.stderr
        )
    else:
        assert result.exit_code == 0
        assert result.stdout.startswith("Usage:") or result.stdout.startswith("DeprecationWarning:")
