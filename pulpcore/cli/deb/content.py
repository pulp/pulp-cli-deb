from typing import IO, Any, Optional, Union

import click
from pulp_glue.common.context import PulpEntityContext
from pulp_glue.common.i18n import get_translation
from pulp_glue.core.context import PulpArtifactContext
from pulp_glue.deb.context import (
    PulpAptRepositoryContext,
    PulpDebGenericContentContext,
    PulpDebInstallerFileIndexContext,
    PulpDebInstallerPackageContext,
    PulpDebPackageContext,
    PulpDebPackageIndexContext,
    PulpDebPackageReleaseComponentContext,
    PulpDebReleaseArchitectureContext,
    PulpDebReleaseComponentContext,
    PulpDebReleaseContext,
    PulpDebReleaseFileContext,
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
    allowed_with_contexts=(PulpDebPackageContext, PulpDebReleaseComponentContext),
)


@pulp_group()
@type_option(
    choices={
        "generic_content": PulpDebGenericContentContext,
        "installer_file_index": PulpDebInstallerFileIndexContext,
        "installer_package": PulpDebInstallerPackageContext,
        "package_release_component": PulpDebPackageReleaseComponentContext,
        "package": PulpDebPackageContext,
        "release_architecture": PulpDebReleaseArchitectureContext,
        "release_component": PulpDebReleaseComponentContext,
        "release_file": PulpDebReleaseFileContext,
        "release": PulpDebReleaseContext,
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
    pulp_option(
        "--architecture",
        allowed_with_contexts=(
            PulpDebInstallerFileIndexContext,
            PulpDebInstallerPackageContext,
            PulpDebPackageIndexContext,
            PulpDebPackageContext,
            PulpDebReleaseArchitectureContext,
        ),
    ),
    pulp_option(
        "--codename",
        allowed_with_contexts=(
            PulpDebReleaseArchitectureContext,
            PulpDebReleaseComponentContext,
            PulpDebReleaseFileContext,
            PulpDebReleaseContext,
        ),
    ),
    pulp_option(
        "--distribution",
        allowed_with_contexts=(
            PulpDebReleaseArchitectureContext,
            PulpDebReleaseComponentContext,
            PulpDebReleaseContext,
        ),
    ),
    pulp_option(
        "--suite",
        allowed_with_contexts=(
            PulpDebReleaseArchitectureContext,
            PulpDebReleaseComponentContext,
            PulpDebReleaseFileContext,
            PulpDebReleaseContext,
        ),
    ),
    pulp_option(
        "--auto-built-package",
        allowed_with_contexts=(
            PulpDebInstallerPackageContext,
            PulpDebPackageContext,
        ),
    ),
    pulp_option(
        "--build-essential",
        allowed_with_contexts=(
            PulpDebInstallerPackageContext,
            PulpDebPackageContext,
        ),
    ),
    pulp_option(
        "--built-using",
        allowed_with_contexts=(
            PulpDebInstallerPackageContext,
            PulpDebPackageContext,
        ),
    ),
    pulp_option(
        "--essential",
        allowed_with_contexts=(
            PulpDebInstallerPackageContext,
            PulpDebPackageContext,
        ),
    ),
    pulp_option(
        "--installed-size",
        allowed_with_contexts=(
            PulpDebInstallerPackageContext,
            PulpDebPackageContext,
        ),
    ),
    pulp_option(
        "--maintainer",
        allowed_with_contexts=(
            PulpDebInstallerPackageContext,
            PulpDebPackageContext,
        ),
    ),
    pulp_option(
        "--origin",
        allowed_with_contexts=(
            PulpDebInstallerPackageContext,
            PulpDebPackageContext,
        ),
    ),
    pulp_option(
        "--package",
        allowed_with_contexts=(
            PulpDebInstallerPackageContext,
            PulpDebPackageReleaseComponentContext,
            PulpDebPackageContext,
        ),
    ),
    pulp_option(
        "--source",
        allowed_with_contexts=(
            PulpDebInstallerPackageContext,
            PulpDebPackageContext,
        ),
    ),
    pulp_option(
        "--tag",
        allowed_with_contexts=(
            PulpDebInstallerPackageContext,
            PulpDebPackageContext,
        ),
    ),
    pulp_option(
        "--version",
        allowed_with_contexts=(
            PulpDebInstallerPackageContext,
            PulpDebPackageContext,
        ),
    ),
    pulp_option(
        "--component",
        allowed_with_contexts=(
            PulpDebInstallerFileIndexContext,
            PulpDebPackageIndexContext,
            PulpDebReleaseComponentContext,
        ),
    ),
    pulp_option(
        "--release-component", allowed_with_contexts=(PulpDebPackageReleaseComponentContext,)
    ),
]
lookup_options = [
    href_option,
    pulp_option(
        "--relative-path",
        callback=_relative_path_callback,
        expose_value=False,
        allowed_with_contexts=(
            PulpDebGenericContentContext,
            PulpDebInstallerFileIndexContext,
            PulpDebPackageIndexContext,
            PulpDebPackageContext,
            PulpDebReleaseFileContext,
        ),
    ),
    pulp_option(
        "--sha256",
        callback=_sha256_callback,
        expose_value=False,
        allowed_with_contexts=(
            PulpDebGenericContentContext,
            PulpDebInstallerFileIndexContext,
            PulpDebPackageIndexContext,
            PulpDebPackageContext,
            PulpDebReleaseFileContext,
        ),
    ),
]

content.add_command(list_command(decorators=list_options))
content.add_command(show_command(decorators=lookup_options))
# create assumes "there exists an Artifact..."
# create is defined for package and expects the sha256 of the artifact.
create_options = [
    pulp_option(
        "--sha256",
        "artifact",
        required=True,
        help=_("Digest of the artifact to use"),
        callback=_sha256_artifact_callback,
        allowed_with_contexts=(PulpDebPackageContext,),
    ),
    pulp_option(
        "--distribution",
        required=True,
        help=_("The APT repo distribution to use"),
        allowed_with_contexts=(PulpDebReleaseComponentContext,),
    ),
    pulp_option(
        "--component",
        required=True,
        help=_("The APT repo component to use"),
        allowed_with_contexts=(PulpDebReleaseComponentContext,),
    ),
    repository_option,
]
content.add_command(
    create_command(
        decorators=create_options,
        allowed_with_contexts=(PulpDebPackageContext, PulpDebReleaseComponentContext),
    )
)


# upload takes a file-argument and creates the entity from it.
# upload currently only works for packages.
# This is a mypy bug getting confused with positional args
# https://github.com/python/mypy/issues/15037
@content.command(allowed_with_contexts=(PulpDebPackageContext,))  # type: ignore [arg-type]
@chunk_size_option
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
    entity_ctx: PulpEntityContext,
    file: IO[bytes],
    chunk_size: int,
    **kwargs: Any,
) -> None:
    """Create a content unit by uploading a file"""
    if isinstance(entity_ctx, PulpDebPackageContext):
        result = entity_ctx.upload(file=file, chunk_size=chunk_size, **kwargs)
    else:
        raise NotImplementedError()
    pulp_ctx.output_result(result)
