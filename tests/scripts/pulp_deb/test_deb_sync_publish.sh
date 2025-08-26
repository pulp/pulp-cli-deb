#!/bin/bash

set -eu

# shellcheck source=tests/scripts/config.source
. "$(dirname "$(dirname "$(realpath "$0")")")/config.source"

ENTITIES_NAME="test_deb_sync_publish"

cleanup() {
  pulp deb remote destroy --name "${ENTITIES_NAME}_remote" || true
  pulp deb repository destroy --name "${ENTITIES_NAME}_repo" || true
  pulp deb distribution destroy --name "${ENTITIES_NAME}_distro" || true
}
trap cleanup EXIT

expect_succ pulp deb remote create \
  --name "${ENTITIES_NAME}_remote" \
  --url "$DEB_REMOTE_URL" \
  --distribution "$DEB_DISTRIBUTION"

expect_succ pulp deb repository create \
  --name "${ENTITIES_NAME}_repo" \
  --remote "${ENTITIES_NAME}_remote"

expect_succ pulp deb repository sync \
  --name "${ENTITIES_NAME}_repo"

if pulp debug has-plugin --name deb --min-version 2.20.0.dev; then
  expect_succ pulp deb repository sync \
    --name "${ENTITIES_NAME}_repo" \
    --optimize

  expect_succ pulp deb repository sync \
    --name "${ENTITIES_NAME}_repo" \
    --no-optimize
fi

expect_succ pulp deb publication create \
  --repository "${ENTITIES_NAME}_repo"

test "$(echo "${OUTPUT}" | jq -r '.checkpoint')" = "false"
test "$(echo "${OUTPUT}" | jq -r '.structured')" = "true"
test "$(echo "${OUTPUT}" | jq -r '.simple')" = "false"

PUBLICATION_HREF=$(echo "$OUTPUT" | jq -r .pulp_href)

expect_succ pulp deb distribution create --name "${ENTITIES_NAME}_distro" \
  --base-path "cli_test_deb_distro" \
  --publication "$PUBLICATION_HREF"

expect_succ pulp deb distribution destroy --name "${ENTITIES_NAME}_distro"
expect_succ pulp deb publication  destroy --href "${PUBLICATION_HREF}"
expect_succ pulp deb remote       destroy --name "${ENTITIES_NAME}_remote"


# Test more unusual publication options:

expect_succ pulp deb publication create \
  --repository "${ENTITIES_NAME}_repo" \
  --checkpoint \
  --simple \
  --no-structured

test "$(echo "${OUTPUT}" | jq -r '.checkpoint')" = "true"
test "$(echo "${OUTPUT}" | jq -r '.structured')" = "false"
test "$(echo "${OUTPUT}" | jq -r '.simple')" = "true"

PUBLICATION_HREF=$(echo "$OUTPUT" | jq -r .pulp_href)
expect_succ pulp deb publication  destroy --href "${PUBLICATION_HREF}"
expect_succ pulp deb repository   destroy --name "${ENTITIES_NAME}_repo"
