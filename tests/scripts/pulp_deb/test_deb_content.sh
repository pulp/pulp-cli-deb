#!/bin/bash

set -eu

# shellcheck source=tests/scripts/config.source
. "$(dirname "$(dirname "$(realpath "$0")")")/config.source"

REPO1_NAME="test_deb_content"
REPO2_NAME="test_deb_content_synced"
DEB_FILENAME="thor_1.0_ppc64.deb"
PACKAGE_HREF=
VERSION_HREF=

cleanup() {
  pulp deb repository destroy --name "${REPO1_NAME}" || true
  pulp deb repository destroy --name "${REPO2_NAME}" || true
  pulp deb remote destroy --name "${REPO1_NAME}" || true
  pulp deb remote destroy --name "${REPO2_NAME}" || true
  # cleanup everything else "asap"
  pulp orphan cleanup --protection-time 0 || true
}
trap cleanup EXIT
cleanup

# Test deb package upload
wget --no-check-certificate "${DEB_REMOTE_URL}/pool/asgard/t/thor/${DEB_FILENAME}"
expect_succ pulp deb content upload --file "${DEB_FILENAME}"
PACKAGE_HREF=$(echo "${OUTPUT}" | jq -r .pulp_href)
expect_succ pulp deb content show --href "${PACKAGE_HREF}"

expect_succ pulp deb remote create --name "${REPO1_NAME}" --url "${DEB_REMOTE_URL}" --distribution "${DEB_DISTRIBUTION}"
expect_succ pulp deb remote show --name "${REPO1_NAME}"
expect_succ pulp deb repository create --name "${REPO1_NAME}" --remote "${REPO1_NAME}"
expect_succ pulp deb repository show --name "${REPO1_NAME}"

expect_succ pulp deb repository content modify \
--repository "${REPO1_NAME}" \
--add-content "[{\"pulp_href\": \"${PACKAGE_HREF}\"}]"
expect_succ pulp deb repository content list --repository "${REPO1_NAME}"
test "$(echo "${OUTPUT}" | jq -r '.[0].pulp_href')" = "${PACKAGE_HREF}"

expect_succ pulp deb repository content modify \
--repository "${REPO1_NAME}" \
--remove-content "[{\"pulp_href\": \"${PACKAGE_HREF}\"}]"
expect_succ pulp deb repository content list --repository "${REPO1_NAME}"
test "$(echo "${OUTPUT}" | jq -r length)" -eq "0"

expect_succ pulp deb repository content add \
--repository "${REPO1_NAME}" \
--package-href "${PACKAGE_HREF}"
expect_succ pulp deb repository content list --repository "${REPO1_NAME}"
test "$(echo "${OUTPUT}" | jq -r '.[0].pulp_href')" = "${PACKAGE_HREF}"

expect_succ pulp deb repository content remove \
--repository "${REPO1_NAME}" \
--package-href "${PACKAGE_HREF}"
expect_succ pulp deb repository content list --repository "${REPO1_NAME}"
test "$(echo "${OUTPUT}" | jq -r length)" -eq "0"

expect_succ pulp deb repository content modify \
--repository "${REPO1_NAME}" \
--remove-content "[{\"pulp_href\": \"${PACKAGE_HREF}\"}]"

expect_succ pulp deb content upload --file "${DEB_FILENAME}" --repository "${REPO1_NAME}" --distribution "my-dist" --component "my-comp"
expect_succ pulp deb repository content list --repository "${REPO1_NAME}"
test "$(echo "${OUTPUT}" | jq -r length)" -eq "1"

VERSION_HREF=$(pulp deb repository version show --repository "${REPO1_NAME}" | jq -r .pulp_href)
expect_succ pulp deb content --type release_component list --repository-version "${VERSION_HREF}"
test "$(echo "${OUTPUT}" | jq -r '.[0].distribution')" = "my-dist"
test "$(echo "${OUTPUT}" | jq -r '.[0].component')" = "my-comp"


# Test list commands with synced repository

expect_succ pulp deb remote create --name "${REPO2_NAME}" --url "${DEB_REMOTE_URL}" --distribution "${DEB_DISTRIBUTION}"
expect_succ pulp deb repository create --name "${REPO2_NAME}" --remote "${REPO2_NAME}"
expect_succ pulp deb repository sync --name "${REPO2_NAME}"
VERSION_HREF=$(pulp deb repository version show --repository "${REPO2_NAME}" | jq -r .pulp_href)

# test list and show for all types
for t in generic_content installer_file_index installer_package package_release_component package release_architecture release_component release_file release
do
  expect_succ pulp deb content -t ${t} list --limit 100 --repository-version "${VERSION_HREF}"
  FOUND=$(echo "${OUTPUT}" | jq -r length)
  case ${t} in
    generic_content)
      test "${FOUND}" -eq "0"
      ;;
    installer_file_index)
      test "${FOUND}" -eq "0"
      ;;
    installer_package)
      test "${FOUND}" -eq "0"
      ;;
    package_release_component)
      test "${FOUND}" -eq "4"
      ;;
    package)
      test "${FOUND}" -eq "4"
      ;;
    release_architecture)
      test "${FOUND}" -eq "2"
      ;;
    release_component)
      test "${FOUND}" -eq "2"
      ;;
    release_file)
      test "${FOUND}" -eq "1"
      ;;
    release)
      test "${FOUND}" -eq "1"
      ;;
    *)
      ;;
  esac
  if test "${FOUND}" -gt "0"
  then
    ENTITY_HREF=$(echo "${OUTPUT}" | jq -r '.[0] | .pulp_href')
    expect_succ pulp deb content -t ${t} show --href "${ENTITY_HREF}"
  fi
done

expect_succ pulp deb content -t package list --limit 100 --repository-version "${VERSION_HREF}"
SYNCED="${OUTPUT}"

expect_succ pulp deb content list --limit 1000
GLOBAL="${OUTPUT}"

# assert the uploaded package is present
echo "${GLOBAL}" | jq -e --arg href "${PACKAGE_HREF}" 'map(.pulp_href) | index($href) != null' >/dev/null

# assert the global list contains every package from the synced repo
jq -n --argjson synced "${SYNCED}" --argjson global "${GLOBAL}" '
  ($global | map(.pulp_href) | unique) as $g
  | ($synced | map(.pulp_href) | unique)
  | all(.; $g | index(.) != null)
' >/dev/null

# make sure the package we've been playing with is cleaned up immediately
expect_succ pulp orphan cleanup --content-hrefs "[\"${PACKAGE_HREF}\"]" --protection-time 0 || true

# Test creating a release_component:
expect_succ pulp deb content --type release_component create --distribution foo --component bar
RELEASE_COMPONENT_HREF=$(echo "${OUTPUT}" | jq -r .pulp_href)
expect_succ pulp orphan cleanup --content-hrefs "[\"${RELEASE_COMPONENT_HREF}\"]" --protection-time 0 || true
