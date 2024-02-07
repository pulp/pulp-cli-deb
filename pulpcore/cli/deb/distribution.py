import gettext

import click
from pulp_glue.deb.context import PulpAptDistributionContext, PulpAptRepositoryContext
from pulpcore.cli.common.generic import (
    PulpCLIContext,
    base_path_contains_option,
    base_path_option,
    create_command,
    destroy_command,
    href_option,
    label_command,
    label_select_option,
    list_command,
    name_option,
    pass_pulp_context,
    resource_option,
    show_command,
    update_command,
)

_ = gettext.gettext


repository_option = resource_option(
    "--repository",
    default_plugin="deb",
    default_type="apt",
    context_table={"deb:apt": PulpAptRepositoryContext},
    help=_(
        "Repository to be used for auto-distributing."
        " Specified as '[[<plugin>:]<type>:]<name>' or as href."
    ),
)


@click.group()
@click.option(
    "-t",
    "--type",
    "distribution_type",
    type=click.Choice(["apt"], case_sensitive=False),
    default="apt",
)
@pass_pulp_context
@click.pass_context
def distribution(ctx: click.Context, pulp_ctx: PulpCLIContext, distribution_type: str) -> None:
    if distribution_type == "apt":
        ctx.obj = PulpAptDistributionContext(pulp_ctx)
    else:
        raise NotImplementedError()


filter_options = [label_select_option, base_path_option, base_path_contains_option]
lookup_options = [href_option, name_option]
update_options = [
    click.option("--base-path"),
    click.option("--publication", help=_("Publication to be served.")),
    repository_option,
]
create_options = update_options + [click.option("--name", required=True)]

distribution.add_command(list_command(decorators=filter_options))
distribution.add_command(show_command(decorators=lookup_options))
distribution.add_command(create_command(decorators=create_options))
distribution.add_command(update_command(decorators=lookup_options + update_options))
distribution.add_command(destroy_command(decorators=lookup_options))
distribution.add_command(label_command())
