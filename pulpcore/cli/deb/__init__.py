from pulpcore.cli.common import main
from pulpcore.cli.common.context import PluginRequirement, PulpContext, pass_pulp_context

from pulpcore.cli.deb.remote import remote
from pulpcore.cli.deb.repository import repository


@main.group()
@pass_pulp_context
def deb(pulp_ctx: PulpContext) -> None:
    pulp_ctx.needs_plugin(PluginRequirement("deb"))


deb.add_command(remote)
deb.add_command(repository)
