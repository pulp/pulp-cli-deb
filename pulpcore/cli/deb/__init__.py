from pulpcore.cli.common import main

from pulpcore.cli.deb.remote import remote
from pulpcore.cli.deb.repository import repository


@main.group()
def deb() -> None:
    pass


deb.add_command(remote)
deb.add_command(repository)
