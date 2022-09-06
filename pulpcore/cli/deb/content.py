from typing import IO, Any, Dict, Optional, Union

import click
from pulp_glue.common.context import PulpEntityContext
from pulp_glue.common.i18n import get_translation
from pulp_glue.core.context import PulpArtifactContext
from pulpcore.cli.deb.context import (
    PulpDebPackageContext,
    PulpAptRepositoryContext,
)

from pulpcore.cli.common.generic import (
    PulpCLIContext,
    chunk_size_option,
    create_command,
    exclude_field_option,
    field_option,
    href_option,
    list_command,
    pass_entity_context,
    pass_pulp_context,
    pulp_group,
    pulp_option,
    resource_option,
    show_command,
    type_option,
)

translation = get_translation(__name__)
_ = translation.gettext


def _relative_path_callback(ctx: click.Context, param: click.Parameter, value: str) -> str:
    if value is not None:
        entity_ctx = ctx.find_object(PulpEntityContext)
        assert entity_ctx is not None
        entity_ctx.entity = {"relative_path": value}
    return value


def _sha256_callback(ctx: click.Context, param: click.Parameter, value: str) -> str:
    if value is not None:
        entity_ctx = ctx.find_object(PulpEntityContext)
        assert entity_ctx is not None
        entity_ctx.entity = {"sha256": value}
    return value


def _sha256_artifact_callback(
    ctx: click.Context, param: click.Parameter, value: Optional[str]
) -> Optional[Union[str, PulpEntityContext]]:
    # Pass None and "" verbatim
    if value:
        pulp_ctx = ctx.find_object(PulpCLIContext)
        assert pulp_ctx is not None
        return PulpArtifactContext(pulp_ctx, entity={"sha256": value})
    return value


repository_option = resource_option(
    "--repository",
    default_plugin="deb",
    default_type="deb",
    context_table={
        "deb:deb": PulpAptRepositoryContext,
    },
    href_pattern=PulpAptRepositoryContext.HREF_PATTERN,
    help=_(
        "Repository to add the content to in the form '[[<plugin>:]<resource_type>:]<name>' or by "
        "href."
    ),
    allowed_with_contexts=(PulpDebPackageContext,),
)


@pulp_group()
@type_option(
    choices={
        "package": PulpDebPackageContext,
    },
    default="package",
    case_sensitive=False,
)
def content() -> None:
    pass


list_options = [
    field_option,
    exclude_field_option,
    pulp_option("--repository-version"),
    pulp_option("--arch", allowed_with_contexts=(PulpDebPackageContext,)),
    pulp_option(
        "--arch-in", "arch__in", multiple=True, allowed_with_contexts=(PulpDebPackageContext,)
    ),
    pulp_option("--arch-ne", "arch__ne", allowed_with_contexts=(PulpDebPackageContext,)),
    pulp_option("--epoch", allowed_with_contexts=(PulpDebPackageContext,)),
    pulp_option(
        "--epoch-in", "epoch__in", multiple=True, allowed_with_contexts=(PulpDebPackageContext,)
    ),
    pulp_option("--epoch-ne", "epoch__ne", allowed_with_contexts=(PulpDebPackageContext,)),
    pulp_option("--package-href", allowed_with_contexts=(PulpDebPackageContext,)),
    pulp_option("--pkgId", allowed_with_contexts=(PulpDebPackageContext,)),
    pulp_option(
        "--pkgId-in",
        "pkgId__in",
        multiple=True,
        allowed_with_contexts=(PulpDebPackageContext,),
    ),
    pulp_option("--release", allowed_with_contexts=(PulpDebPackageContext,)),
    pulp_option(
        "--release-in", "release__in", multiple=True, allowed_with_contexts=(PulpDebPackageContext,)
    ),
    pulp_option("--release-ne", "release__ne", allowed_with_contexts=(PulpDebPackageContext,)),
    pulp_option(
        "--version-in", "version__in", multiple=True, allowed_with_contexts=(PulpDebPackageContext,)
    ),
    pulp_option("--version-ne", "version__ne", allowed_with_contexts=(PulpDebPackageContext,)),
]
lookup_options = [
    href_option,
    pulp_option(
        "--relative-path",
        callback=_relative_path_callback,
        expose_value=False,
        allowed_with_contexts=(PulpDebPackageContext,),
    ),
    pulp_option(
        "--sha256",
        callback=_sha256_callback,
        expose_value=False,
        allowed_with_contexts=(
            PulpDebPackageContext,
        ),
    ),
]

content.add_command(list_command(decorators=list_options))
content.add_command(show_command(decorators=lookup_options))
# create assumes "there exists an Artifact..."
# create is defined for package, modulemd and modulemd_defaults.  The implications for modulemd
# and modulemd_defaults are generally not what the user expects. Therefore, leaving those two
# endpoints hidden until we have a better handle on what we should really be doing.
# See https://github.com/pulp/pulp_deb/issues/2229 and https://github.com/pulp/pulp_deb/issues/2534
create_options = [
    pulp_option(
        "--relative-path",
        allowed_with_contexts=(PulpDebPackageContext,),
    ),
    pulp_option(
        "--sha256",
        "artifact",
        required=True,
        help=_("Digest of the artifact to use"),
        callback=_sha256_artifact_callback,
        allowed_with_contexts=(PulpDebPackageContext,),
    ),
    repository_option,
]
content.add_command(
    create_command(
        decorators=create_options,
        allowed_with_contexts=(PulpDebPackageContext,),
    )
)


# upload takes a file-argument and creates the entity from it.
# upload currently only works for advisory/package,
# see https://github.com/pulp/pulp_deb/issues/2534
@content.command(
    allowed_with_contexts=(
        PulpDebPackageContext,
    )
)
@chunk_size_option
@pulp_option(
    "--relative-path",
    help=_("Relative path within a distribution of the entity"),
    allowed_with_contexts=(PulpDebPackageContext,),
)
@pulp_option(
    "--file",
    type=click.File("rb"),
    required=True,
    help=_("An DEB binary"),
    allowed_with_contexts=(PulpDebPackageContext,),
)
@repository_option
@pass_entity_context
@pass_pulp_context
def upload(
    pulp_ctx: PulpCLIContext,
    entity_ctx: Union[
        PulpDebPackageContext,
    ],
    file: IO[bytes],
    chunk_size: int,
    **kwargs: Any,
) -> None:
    """Create a content unit by uploading a file"""
    body: Dict[str, Any]
    if isinstance(entity_ctx, PulpDebPackageContext):
        result = entity_ctx.upload(file=file, chunk_size=chunk_size, **kwargs)
    else:
        raise NotImplementedError()
    pulp_ctx.output_result(result)
