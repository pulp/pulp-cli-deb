_taken from `pulp-cli` [repository](https://github.com/pulp/pulp-cli/blob/main/releasing.md)_

# Releasing (for internal use)

## Create new y-Release Branch

1. Trigger the [Create Release Branch](https://github.com/pulp/pulp-cli-deb/actions/workflows/release_branch.yml) action.
1. Review (if need to, repair) and merge the "Bumb Version" PR.

## Create a new Release from a Release Branch

1. Trigger the [pulp-cli Release](https://github.com/pulp/pulp-cli-deb/actions/workflows/release.yml) action with the release branch selected.
1. Monitor the release and build jobs and then check PyPI to make sure the package has been uploaded and the docs updated.
1. Announce the release at https://discourse.pulpproject.org/c/announcements/6.
1. Wait for nightlies (or trigger the [collect changes][https://github.com/pulp/pulp-cli-deb/actions/workflows/collect_changes.yml] workflow) to pickup new changelogs.
1. Review (if need to, repair) and merge the "Update Changelog" PR.
