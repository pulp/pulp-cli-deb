from pulpcore.cli.common import main
from pulpcore.cli.common.context import PluginRequirement
from pulpcore.cli.common.generic import PulpCLIContext, pass_pulp_context

from pulpcore.cli.deb.distribution import distribution
from pulpcore.cli.deb.publication import publication
from pulpcore.cli.deb.remote import remote
from pulpcore.cli.deb.repository import repository
from pulpcore.cli.deb.content import content


@main.group()
@pass_pulp_context
def deb(pulp_ctx: PulpCLIContext) -> None:
    pulp_ctx.needs_plugin(PluginRequirement("deb"))


deb.add_command(distribution)
deb.add_command(publication)
deb.add_command(remote)
deb.add_command(repository)
deb.add_command(content)
