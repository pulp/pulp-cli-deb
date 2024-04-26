from typing import Any, Dict, Optional

import click
import schema as s
from pulp_glue.common.context import (
    EntityFieldDefinition,
    PluginRequirement,
    PulpContext,
    PulpEntityContext,
    PulpRepositoryContext,
)
from pulp_glue.common.i18n import get_translation
from pulp_glue.deb.context import (
    PulpAptRemoteContext,
    PulpAptRepositoryContext,
    PulpDebPackageContext,
)
from pulpcore.cli.common.generic import (
    PulpCLIContext,
    create_command,
    create_content_json_callback,
    destroy_command,
    href_option,
    label_command,
    label_select_option,
    list_command,
    name_option,
    pass_pulp_context,
    pass_repository_context,
    pulp_option,
    repository_content_command,
    repository_href_option,
    repository_lookup_option,
    resource_option,
    retained_versions_option,
    show_command,
    update_command,
    version_command,
)
from pulpcore.cli.core.generic import task_command

translation = get_translation(__name__)
_ = translation.gettext


def _content_callback(ctx: click.Context, param: click.Parameter, value: Any) -> Any:
    if value:
        pulp_ctx = ctx.find_object(PulpContext)
        assert pulp_ctx is not None
        ctx.obj = PulpDebPackageContext(pulp_ctx, pulp_href=value)
    return value


CONTENT_LIST_SCHEMA = s.Schema([{"pulp_href": str}])

package_options = [
    click.option(
        "--package-href",
        callback=_content_callback,
        expose_value=False,
        help=_("Href of the deb package to use"),
    )
]

content_json_callback = create_content_json_callback(
    PulpDebPackageContext, schema=CONTENT_LIST_SCHEMA
)
modify_options = [
    click.option(
        "--add-content",
        callback=content_json_callback,
        help=_(
            """JSON string with a list of objects to add to the repository.
            Each object must containt the following keys: "pulp_href".
            The argument prefixed with the '@' can be the patch to a JSON
            file with a list of objects."""
        ),
    ),
    click.option(
        "--remove-content",
        callback=content_json_callback,
        help=_(
            """JSON string with a list of objects to remove from the repositoy.
            Each object must contain the following keys: "pulp_href".
            The argument prefixed with the '@' can be the path to a JSON
            file with a list of objects."""
        ),
    ),
]

remote_option = resource_option(
    "--remote",
    default_plugin="deb",
    default_type="apt",
    context_table={"deb:apt": PulpAptRemoteContext},
    needs_plugins=[PluginRequirement("deb", specifier=">=2.12.0")],
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
nested_lookup_options = [repository_href_option, repository_lookup_option]
update_options = [
    click.option("--description"),
    remote_option,
    # pulp_option(
    #     "--autopublish/--no-autopublish",
    #     needs_plugins=[PluginRequirement("deb", specifier=">=999.0.0")],
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
repository.add_command(
    repository_content_command(
        contexts={"package": PulpDebPackageContext},
        add_decorators=package_options,
        remove_decorators=package_options,
        modify_decorators=modify_options,
    )
)


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
    needs_plugins=[PluginRequirement("deb", specifier=">=2.20.0")],
)
@pass_repository_context
def sync(
    repository_ctx: PulpRepositoryContext,
    remote: EntityFieldDefinition,
    mirror: Optional[bool],
    optimize: Optional[bool],
) -> None:
    repository = repository_ctx.entity

    body: Dict[str, Any] = {}

    if mirror is not None:
        body["mirror"] = mirror

    if optimize is not None:
        body["optimize"] = optimize

    if isinstance(remote, PulpEntityContext):
        body["remote"] = remote
    elif repository["remote"] is None:
        raise click.ClickException(
            _(
                "Repository '{name}' does not have a default remote. "
                "Please specify with '--remote'."
            ).format(name=repository["name"])
        )

    repository_ctx.sync(body=body)
