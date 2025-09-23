from typing import Any

import click
from pulp_glue.deb.context import PulpAptRemoteContext, PulpDebACSContext
from pulpcore.cli.common.generic import pulp_group

from pulpcore.cli.common.acs import acs_command
from pulpcore.cli.deb.content import content
from pulpcore.cli.deb.distribution import distribution
from pulpcore.cli.deb.publication import publication
from pulpcore.cli.deb.remote import remote
from pulpcore.cli.deb.repository import repository

__version__ = "0.5.0.dev"


@pulp_group(name="deb")
def deb_group() -> None:
    pass


def mount(main: click.Group, **kwargs: Any) -> None:
    deb_group.add_command(distribution)
    deb_group.add_command(publication)
    deb_group.add_command(remote)
    deb_group.add_command(repository)
    deb_group.add_command(content)
    deb_group.add_command(
        acs_command(
            acs_contexts={"deb": PulpDebACSContext},
            remote_context_table={"deb:apt": PulpAptRemoteContext},
        )
    )
    main.add_command(deb_group)
