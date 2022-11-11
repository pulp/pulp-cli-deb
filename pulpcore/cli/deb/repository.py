from typing import Any, Dict, Optional

import click
from pulpcore.cli.common.context import (
    EntityFieldDefinition,
    PluginRequirement,
    PulpEntityContext,
    PulpRepositoryContext,
)
from pulpcore.cli.common.generic import (
    PulpCLIContext,
    create_command,
    destroy_command,
    href_option,
    label_command,
    label_select_option,
    list_command,
    name_option,
    pass_pulp_context,
    pass_repository_context,
    pulp_option,
    repository_href_option,
    repository_option,
    resource_option,
    retained_versions_option,
    show_command,
    update_command,
    version_command,
)
from pulpcore.cli.common.i18n import get_translation
from pulpcore.cli.core.generic import task_command

from pulpcore.cli.deb.context import PulpAptRemoteContext, PulpAptRepositoryContext

translation = get_translation(__name__)
_ = translation.gettext


remote_option = resource_option(
    "--remote",
    default_plugin="deb",
    default_type="apt",
    context_table={"deb:apt": PulpAptRemoteContext},
    needs_plugins=[PluginRequirement("deb", "2.12.0")],
)


@click.group()
@click.option(
    "-t",
    "--type",
    "repo_type",
    type=click.Choice(["apt"], case_sensitive=False),
    default="apt",
)
@pass_pulp_context
@click.pass_context
def repository(ctx: click.Context, pulp_ctx: PulpCLIContext, repo_type: str) -> None:
    if repo_type == "apt":
        ctx.obj = PulpAptRepositoryContext(pulp_ctx)
    else:
        raise NotImplementedError()


lookup_options = [href_option, name_option]
nested_lookup_options = [repository_href_option, repository_option]
update_options = [
    click.option("--description"),
    remote_option,
    # pulp_option(
    #     "--autopublish/--no-autopublish",
    #     needs_plugins=[PluginRequirement("deb", "999.0.0")],
    #     default=None,
    # ),
    retained_versions_option,
]
create_options = update_options + [click.option("--name", required=True)]

repository.add_command(list_command(decorators=[label_select_option]))
repository.add_command(show_command(decorators=lookup_options))
repository.add_command(create_command(decorators=create_options))
repository.add_command(update_command(decorators=lookup_options + update_options))
repository.add_command(destroy_command(decorators=lookup_options))
repository.add_command(task_command(decorators=nested_lookup_options))
repository.add_command(version_command(decorators=nested_lookup_options))
repository.add_command(label_command(decorators=nested_lookup_options))


@repository.command()
@name_option
@href_option
@remote_option
@click.option(
    "--mirror/--no-mirror",
    default=None,
    help=(
        "Using mirror mode, will remove all content that is not present in the remote repository "
        "during sync. When disabled, the sync is purely additive."
    ),
)
@pulp_option(
    "--optimize/--no-optimize",
    default=None,
    help=(
        "Using optimize sync, will skip the processing of metadata if the checksum has not changed "
        "since the last sync. This greately improves re-sync performance in such cases. Disable if "
        "the sync result does not match expectations."
    ),
    needs_plugins=[PluginRequirement("deb", min="2.20.0.dev")],
)
@pass_repository_context
def sync(
    repository_ctx: PulpRepositoryContext,
    remote: EntityFieldDefinition,
    mirror: Optional[bool],
    optimize: Optional[bool],
) -> None:
    repository = repository_ctx.entity
    repository_href = repository_ctx.pulp_href

    body: Dict[str, Any] = {}

    if mirror is not None:
        body["mirror"] = mirror

    if optimize is not None:
        body["optimize"] = optimize

    if isinstance(remote, PulpEntityContext):
        body["remote"] = remote.pulp_href
    elif repository["remote"] is None:
        raise click.ClickException(
            _(
                "Repository '{name}' does not have a default remote. "
                "Please specify with '--remote'."
            ).format(name=repository["name"])
        )

    repository_ctx.sync(
        href=repository_href,
        body=body,
    )
