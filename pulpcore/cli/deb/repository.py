import gettext
from typing import Any, Dict, Optional

import click
from pulpcore.cli.common.context import (
    EntityFieldDefinition,
    PluginRequirement,
    PulpContext,
    PulpEntityContext,
    PulpRepositoryContext,
    pass_pulp_context,
    pass_repository_context,
)
from pulpcore.cli.common.generic import (
    create_command,
    destroy_command,
    href_option,
    label_command,
    label_select_option,
    list_command,
    name_option,
    repository_href_option,
    repository_option,
    resource_option,
    retained_versions_option,
    show_command,
    update_command,
    version_command,
)
from pulpcore.cli.core.generic import task_command

from pulpcore.cli.deb.context import PulpAptRemoteContext, PulpAptRepositoryContext

_ = gettext.gettext


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
def repository(ctx: click.Context, pulp_ctx: PulpContext, repo_type: str) -> None:
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
@click.option("--mirror/--no-mirror", default=None)
@pass_repository_context
def sync(
    repository_ctx: PulpRepositoryContext,
    remote: EntityFieldDefinition,
    mirror: Optional[bool],
) -> None:
    repository = repository_ctx.entity
    repository_href = repository_ctx.pulp_href

    body: Dict[str, Any] = {}

    if mirror is not None:
        body["mirror"] = mirror

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
