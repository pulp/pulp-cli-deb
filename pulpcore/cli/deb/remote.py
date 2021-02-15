import click
from pulpcore.cli.common.context import PulpContext, pass_entity_context, pass_pulp_context
from pulpcore.cli.common.generic import (
    destroy_command,
    href_option,
    list_command,
    name_option,
    show_command,
)

from pulpcore.cli.deb.context import PulpAptRemoteContext


@click.group()
@click.option(
    "-t",
    "--type",
    "remote_type",
    type=click.Choice(["apt"], case_sensitive=False),
    default="apt",
)
@pass_pulp_context
@click.pass_context
def remote(ctx: click.Context, pulp_ctx: PulpContext, remote_type: str) -> None:
    if remote_type == "apt":
        ctx.obj = PulpAptRemoteContext(pulp_ctx)
    else:
        raise NotImplementedError()


lookup_options = [name_option, href_option]

remote.add_command(list_command())
remote.add_command(show_command(decorators=lookup_options))
remote.add_command(destroy_command(decorators=lookup_options))


@remote.command()
@click.option("--name", required=True)
@click.option("--url", required=True)
@click.option("--distributions", required=True)
@pass_entity_context
@pass_pulp_context
def create(
    pulp_ctx: PulpContext, remote_ctx: PulpAptRemoteContext, name: str, url: str, distributions: str
) -> None:
    remote = {
        "name": name,
        "url": url,
        "distributions": distributions,
    }
    result = remote_ctx.create(body=remote)
    pulp_ctx.output_result(result)
