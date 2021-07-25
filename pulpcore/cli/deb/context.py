import gettext

from pulpcore.cli.common.context import (
    PulpEntityContext,
    PulpRepositoryContext,
    PulpRepositoryVersionContext,
    registered_repository_contexts,
)

_ = gettext.gettext


class PulpAptRemoteContext(PulpEntityContext):
    ENTITY = "remote"
    HREF = "deb_apt_remote_href"
    LIST_ID = "remotes_deb_apt_list"
    CREATE_ID = "remotes_deb_apt_create"
    UPDATE_ID = "remotes_deb_apt_update"
    DELETE_ID = "remotes_deb_apt_delete"


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
    UPDATE_ID = "repositories_deb_apt_update"
    DELETE_ID = "repositories_deb_apt_delete"
    SYNC_ID = "repositories_deb_apt_sync"
    VERSION_CONTEXT = PulpAptRepositoryVersionContext


registered_repository_contexts["deb:apt"] = PulpAptRepositoryContext
