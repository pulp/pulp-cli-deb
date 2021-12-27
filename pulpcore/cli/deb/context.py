import gettext
from typing import ClassVar, Set

import click
from pulpcore.cli.common.context import (
    EntityDefinition,
    PulpEntityContext,
    PulpRepositoryContext,
    PulpRepositoryVersionContext,
    registered_repository_contexts,
)

_ = gettext.gettext


class PulpAptDistributionContext(PulpEntityContext):
    ENTITY = _("apt distribution")
    ENTITIES = _("apt distributions")
    HREF = "deb_apt_distribution_href"
    LIST_ID = "distributions_deb_apt_list"
    READ_ID = "distributions_deb_apt_read"
    CREATE_ID = "distributions_deb_apt_create"
    UPDATE_ID = "distributions_deb_apt_partial_update"
    DELETE_ID = "distributions_deb_apt_delete"


class PulpAptPublicationContext(PulpEntityContext):
    ENTITY = _("apt publication")
    ENTITIES = _("apt publications")
    HREF = "deb_apt_publication_href"
    LIST_ID = "publications_deb_apt_list"
    READ_ID = "publications_deb_apt_read"
    CREATE_ID = "publications_deb_apt_create"
    DELETE_ID = "publications_deb_apt_delete"

    def preprocess_body(self, body: EntityDefinition) -> EntityDefinition:
        body = super().preprocess_body(body)
        version = body.pop("version", None)
        if version is not None:
            repository_href = body.pop("repository")
            body["repository_version"] = f"{repository_href}versions/{version}/"
        return body


class PulpVerbatimPublicationContext(PulpEntityContext):
    ENTITY = _("verbatim publication")
    ENTITIES = _("verbatim publications")
    HREF = "deb_verbatim_publication_href"
    LIST_ID = "publications_deb_verbatim_list"
    READ_ID = "publications_deb_verbatim_read"
    CREATE_ID = "publications_deb_verbatim_create"
    DELETE_ID = "publications_deb_verbatim_delete"
    APT_ONLY: ClassVar[Set[str]] = {"simple", "structured", "signing_service"}

    def preprocess_body(self, body: EntityDefinition) -> EntityDefinition:
        body = super().preprocess_body(body)
        fields = self.APT_ONLY.intersection(body.keys())
        if fields:
            raise click.ClickException(
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
    LIST_ID = "remotes_deb_apt_list"
    READ_ID = "remotes_deb_apt_read"
    CREATE_ID = "remotes_deb_apt_create"
    UPDATE_ID = "remotes_deb_apt_partial_update"
    DELETE_ID = "remotes_deb_apt_delete"
    NULLABLES = {"architectures", "components"}

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
        if field is not None and field != ():
            string_field = " ".join(field).strip()
            body[field_name] = string_field if string_field else None

    def preprocess_body(self, body: EntityDefinition) -> EntityDefinition:
        body = super().preprocess_body(body)
        self.tuple_to_whitespace_separated_string("distributions", body)
        self.tuple_to_whitespace_separated_string("components", body)
        self.tuple_to_whitespace_separated_string("architectures", body)
        return body


class PulpAptRepositoryVersionContext(PulpRepositoryVersionContext):
    HREF = "deb_apt_repository_version_href"
    REPOSITORY_HREF = "deb_apt_repository_href"
    LIST_ID = "repositories_deb_apt_versions_list"
    READ_ID = "repositories_deb_apt_versions_read"
    DELETE_ID = "repositories_deb_apt_versions_delete"


class PulpAptRepositoryContext(PulpRepositoryContext):
    HREF = "deb_apt_repository_href"
    LIST_ID = "repositories_deb_apt_list"
    READ_ID = "repositories_deb_apt_read"
    CREATE_ID = "repositories_deb_apt_create"
    UPDATE_ID = "repositories_deb_apt_partial_update"
    DELETE_ID = "repositories_deb_apt_delete"
    SYNC_ID = "repositories_deb_apt_sync"
    VERSION_CONTEXT = PulpAptRepositoryVersionContext


registered_repository_contexts["deb:apt"] = PulpAptRepositoryContext
