import click
from pulp_glue.common.i18n import get_translation
from pulp_glue.deb.context import PulpAptRemoteContext
from pulpcore.cli.common.generic import (
    PulpCLIContext,
    common_remote_create_options,
    common_remote_update_options,
    create_command,
    destroy_command,
    href_option,
    label_command,
    label_select_option,
    list_command,
    load_string_callback,
    name_option,
    pass_pulp_context,
    show_command,
    update_command,
)

translation = get_translation(__name__)
_ = translation.gettext


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
def remote(ctx: click.Context, pulp_ctx: PulpCLIContext, remote_type: str) -> None:
    if remote_type == "apt":
        ctx.obj = PulpAptRemoteContext(pulp_ctx)
    else:
        raise NotImplementedError()


lookup_options = [href_option, name_option]
apt_remote_common_options = [
    click.option(
        "--policy", type=click.Choice(["immediate", "on_demand", "streamed"], case_sensitive=False)
    ),
    click.option(
        "--component",
        "components",
        multiple=True,
        help=_(
            "Component to sync; can be specified multiple times. "
            "Will sync all available if specified once with the empty string."
        ),
    ),
    click.option(
        "--architecture",
        "architectures",
        multiple=True,
        help=_(
            "Architecture to sync; can be specified multiple times. "
            "Will sync all available if specified once with the empty string."
        ),
    ),
]

distribution_help = _("Distribution to sync; can be specified multiple times.")
apt_remote_create_options = (
    common_remote_create_options
    + apt_remote_common_options
    + [
        click.option(
            "--distribution",
            "distributions",
            multiple=True,
            required=True,
            help=distribution_help,
        ),
        click.option(
            "--gpgkey",
            help=_("Gpg public key to verify origin releases against or @file containing same."),
            callback=load_string_callback,
        ),
    ]
)
apt_remote_update_options = (
    lookup_options
    + common_remote_update_options
    + apt_remote_common_options
    + [
        click.option(
            "--distribution",
            "distributions",
            multiple=True,
            help=distribution_help,
        ),
        click.option(
            "--gpgkey",
            help=_("Gpg public key to verify origin releases against or @file containing same."),
            callback=load_string_callback,
        ),
    ]
)

remote.add_command(list_command(decorators=[label_select_option]))
remote.add_command(show_command(decorators=lookup_options))
remote.add_command(create_command(decorators=apt_remote_create_options))
remote.add_command(update_command(decorators=apt_remote_update_options))
remote.add_command(destroy_command(decorators=lookup_options))
remote.add_command(label_command())
