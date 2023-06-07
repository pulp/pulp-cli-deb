import gettext

import click
from pulpcore.cli.common.generic import (
    PulpCLIContext,
    create_command,
    destroy_command,
    href_option,
    list_command,
    pass_pulp_context,
    publication_filter_options,
    resource_option,
    show_command,
)
from pulpcore.cli.core.context import PulpSigningServiceContext

from pulpcore.cli.deb.context import (
    PulpAptPublicationContext,
    PulpAptRepositoryContext,
    PulpVerbatimPublicationContext,
)

_ = gettext.gettext


repository_option = resource_option(
    "--repository",
    default_plugin="deb",
    default_type="apt",
    context_table={"deb:apt": PulpAptRepositoryContext},
)


@click.group()
@click.option(
    "-t",
    "--type",
    "publication_type",
    type=click.Choice(["apt", "verbatim"], case_sensitive=False),
    default="apt",
)
@pass_pulp_context
@click.pass_context
def publication(ctx: click.Context, pulp_ctx: PulpCLIContext, publication_type: str) -> None:
    if publication_type == "apt":
        ctx.obj = PulpAptPublicationContext(pulp_ctx)
    elif publication_type == "verbatim":
        ctx.obj = PulpVerbatimPublicationContext(pulp_ctx)
    else:
        raise NotImplementedError()


lookup_options = [href_option]
create_options = [
    repository_option,
    click.option(
        "--version", type=int, help=_("a repository version number, leave blank for latest")
    ),
    click.option(
        "--simple",
        is_flag=True,
        default=None,
        help=_("Apt only: Activate simple publishing mode"),
    ),
    click.option(
        "--structured",
        is_flag=True,
        default=None,
        help=_("Apt only: Activate structured publishing mode"),
    ),
    resource_option(
        "--signing-service",
        default_plugin="deb",
        default_type="apt",
        context_table={"deb:apt": PulpSigningServiceContext},
        href_pattern=PulpSigningServiceContext.HREF_PATTERN,
        help=_("Apt only: Signing service to use, pass in name or href"),
    ),
]
publication.add_command(list_command(decorators=publication_filter_options))
publication.add_command(show_command(decorators=lookup_options))
publication.add_command(create_command(decorators=create_options))
publication.add_command(destroy_command(decorators=lookup_options))
