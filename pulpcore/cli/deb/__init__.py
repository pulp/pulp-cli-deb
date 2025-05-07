from typing import Any

import click
from pulpcore.cli.common.generic import pulp_group

from pulpcore.cli.deb.content import content
from pulpcore.cli.deb.distribution import distribution
from pulpcore.cli.deb.publication import publication
from pulpcore.cli.deb.remote import remote
from pulpcore.cli.deb.repository import repository

__version__ = "0.3.3"


@pulp_group(name="deb")
def deb_group() -> None:
    pass


def mount(main: click.Group, **kwargs: Any) -> None:
    deb_group.add_command(distribution)
    deb_group.add_command(publication)
    deb_group.add_command(remote)
    deb_group.add_command(repository)
    deb_group.add_command(content)
    main.add_command(deb_group)
