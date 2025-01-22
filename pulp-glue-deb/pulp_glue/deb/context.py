from typing import ClassVar, Set

from pulp_glue.common.context import (  # type: ignore[attr-defined]
    EntityDefinition,
    PluginRequirement,
    PulpContentContext,
    PulpEntityContext,
    PulpException,
    PulpRepositoryContext,
    PulpRepositoryVersionContext,
)
from pulp_glue.common.i18n import get_translation

translation = get_translation(__name__)
_ = translation.gettext


class PulpDebGenericContentContext(PulpContentContext):
    ENTITY = "deb generic content"
    ENTITIES = "deb generic contents"
    HREF = "deb_generic_content_href"
    ID_PREFIX = "content_deb_generic_contents"
    NEEDS_PLUGINS = [PluginRequirement("deb")]
    PLUGIN = "deb"
    RESOURCE_TYPE = "generic_content"


class PulpDebInstallerFileIndexContext(PulpContentContext):
    ENTITY = "deb installer file index"
    ENTITIES = "deb installer file indices"
    HREF = "deb_installer_file_index_href"
    ID_PREFIX = "content_deb_installer_file_indices"
    NEEDS_PLUGINS = [PluginRequirement("deb")]
    PLUGIN = "deb"
    RESOURCE_TYPE = "installer_file_index"


class PulpDebInstallerPackageContext(PulpContentContext):
    ENTITY = "deb installer package"
    ENTITIES = "deb installer packages"
    HREF = "deb_installer_package_href"
    ID_PREFIX = "content_deb_installer_packages"
    NEEDS_PLUGINS = [PluginRequirement("deb")]
    PLUGIN = "deb"
    RESOURCE_TYPE = "installer_package"


class PulpDebPackageIndexContext(PulpContentContext):
    ENTITY = "deb package index"
    ENTITIES = "deb package indices"
    HREF = "deb_package_index_href"
    ID_PREFIX = "content_deb_package_indices"
    NEEDS_PLUGINS = [PluginRequirement("deb")]
    PLUGIN = "deb"
    RESOURCE_TYPE = "package_index"


class PulpDebPackageReleaseComponentContext(PulpContentContext):
    ENTITY = "deb package release component"
    ENTITIES = "deb package release components"
    HREF = "deb_package_release_component_href"
    ID_PREFIX = "content_deb_package_release_components"
    NEEDS_PLUGINS = [PluginRequirement("deb")]
    PLUGIN = "deb"
    RESOURCE_TYPE = "package_release_component"


class PulpDebPackageContext(PulpContentContext):
    CAPABILITIES = {"upload": []}
    ENTITY = "deb package"
    ENTITIES = "deb packages"
    HREF = "deb_package_href"
    ID_PREFIX = "content_deb_packages"
    NEEDS_PLUGINS = [PluginRequirement("deb")]
    PLUGIN = "deb"
    RESOURCE_TYPE = "package"


class PulpDebReleaseArchitectureContext(PulpContentContext):
    ENTITY = "deb release architecture"
    ENTITIES = "deb release architectures"
    HREF = "deb_release_architecture_href"
    ID_PREFIX = "content_deb_release_architectures"
    NEEDS_PLUGINS = [PluginRequirement("deb")]
    PLUGIN = "deb"
    RESOURCE_TYPE = "release_architecture"


class PulpDebReleaseComponentContext(PulpContentContext):
    ENTITY = "deb release component"
    ENTITIES = "deb release components"
    HREF = "deb_release_component_href"
    ID_PREFIX = "content_deb_release_components"
    NEEDS_PLUGINS = [PluginRequirement("deb")]
    PLUGIN = "deb"
    RESOURCE_TYPE = "release_component"


class PulpDebReleaseFileContext(PulpContentContext):
    ENTITY = "deb release file"
    ENTITIES = "deb release files"
    HREF = "deb_release_file_href"
    ID_PREFIX = "content_deb_release_files"
    NEEDS_PLUGINS = [PluginRequirement("deb")]
    PLUGIN = "deb"
    RESOURCE_TYPE = "release_file"


class PulpDebReleaseContext(PulpContentContext):
    ENTITY = "deb release"
    ENTITIES = "deb releases"
    HREF = "deb_release_href"
    ID_PREFIX = "content_deb_releases"
    NEEDS_PLUGINS = [PluginRequirement("deb")]
    PLUGIN = "deb"
    RESOURCE_TYPE = "release"


class PulpAptDistributionContext(PulpEntityContext):
    ENTITY = _("apt distribution")
    ENTITIES = _("apt distributions")
    HREF = "deb_apt_distribution_href"
    ID_PREFIX = "distributions_deb_apt"
    NEEDS_PLUGINS = [PluginRequirement("deb")]
    PLUGIN = "deb"
    RESOURCE_TYPE = "apt"


class PulpAptPublicationContext(PulpEntityContext):
    ENTITY = _("apt publication")
    ENTITIES = _("apt publications")
    HREF = "deb_apt_publication_href"
    ID_PREFIX = "publications_deb_apt"
    NEEDS_PLUGINS = [PluginRequirement("deb")]
    PLUGIN = "deb"
    RESOURCE_TYPE = "apt"

    def preprocess_entity(self, body: EntityDefinition, partial: bool = False) -> EntityDefinition:
        body = super().preprocess_entity(body)
        version = body.pop("version", None)
        if version is not None:
            repository_href = body.pop("repository")
            body["repository_version"] = f"{repository_href}versions/{version}/"
        return body


class PulpVerbatimPublicationContext(PulpEntityContext):
    APT_ONLY: ClassVar[Set[str]] = {"simple", "structured", "signing_service"}
    ENTITY = _("verbatim publication")
    ENTITIES = _("verbatim publications")
    HREF = "deb_verbatim_publication_href"
    ID_PREFIX = "publications_deb_verbatim"
    NEEDS_PLUGINS = [PluginRequirement("deb")]
    PLUGIN = "deb"
    RESOURCE_TYPE = "verbatim"

    def preprocess_entity(self, body: EntityDefinition, partial: bool = False) -> EntityDefinition:
        body = super().preprocess_entity(body)
        fields = self.APT_ONLY.intersection(body.keys())
        if fields:
            raise PulpException(
                _("{} can't be used when creating VerbatimPublications").format(fields)
            )
        version = body.pop("version", None)
        if version is not None:
            repository_href = body.pop("repository")
            body["repository_version"] = f"{repository_href}versions/{version}/"
        return body


class PulpAptRemoteContext(PulpEntityContext):
    ENTITY = _("apt remote")
    ENTITIES = _("apt remotes")
    HREF = "deb_apt_remote_href"
    ID_PREFIX = "remotes_deb_apt"
    NEEDS_PLUGINS = [PluginRequirement("deb")]
    NULLABLES = {"architectures", "components"}
    PLUGIN = "deb"
    RESOURCE_TYPE = "apt"

    @staticmethod
    def tuple_to_whitespace_separated_string(field_name: str, body: EntityDefinition) -> None:
        """
        Safely turns a tuple contained in body[field_name] into a whitespace separated string.
        If body[field_name] contains None or (), then field_name is dropped from body.
        If we end up with an empty string, we use None instead.
        All conversions happen in place.
        If body[field_name] does not contain a tuple, the behaviour is undefined.
        """
        field = body.pop(field_name, None)
        if field:
            string_field = " ".join(field).strip()
            body[field_name] = string_field if string_field else None

    def preprocess_entity(self, body: EntityDefinition, partial: bool = False) -> EntityDefinition:
        body = super().preprocess_entity(body)
        self.tuple_to_whitespace_separated_string("distributions", body)
        if "distributions" in body and body["distributions"] is None:
            raise PulpException("Must have at least one distribution for remote.")
        self.tuple_to_whitespace_separated_string("components", body)
        self.tuple_to_whitespace_separated_string("architectures", body)
        return body


class PulpAptRepositoryVersionContext(PulpRepositoryVersionContext):
    HREF = "deb_apt_repository_version_href"
    REPOSITORY_HREF = "deb_apt_repository_href"
    ID_PREFIX = "repositories_deb_apt_versions"
    NEEDS_PLUGINS = [PluginRequirement("deb")]


class PulpAptRepositoryContext(PulpRepositoryContext):
    ENTITY = _("apt repository")
    ENTITIES = _("apt repositories")
    HREF = "deb_apt_repository_href"
    ID_PREFIX = "repositories_deb_apt"
    NEEDS_PLUGINS = [PluginRequirement("deb")]
    PLUGIN = "deb"
    RESOURCE_TYPE = "apt"
    VERSION_CONTEXT = PulpAptRepositoryVersionContext
