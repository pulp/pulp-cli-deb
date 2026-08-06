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

if pulp debug has-plugin --name deb --specifier ">=3.12.0.dev"; then
  expect_succ pulp deb repository create \
    --name "${ENTITIES_NAME}_repo" \
    --remote "${ENTITIES_NAME}_remote" \
    --excluded-package-metadata-field "Phased-Update-Percentage"
  assert "$(echo "$OUTPUT" | jq -c .excluded_package_metadata_fields)" == \
    '["Phased-Update-Percentage"]'
else
  expect_succ pulp deb repository create \
    --name "${ENTITIES_NAME}_repo" \
    --remote "${ENTITIES_NAME}_remote"
fi

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

if pulp debug has-plugin --name deb --specifier ">=3.11.0"; then
  expect_succ pulp deb publication create \
    --repository "${ENTITIES_NAME}_repo" \
    --simple \
    --excluded-package-metadata-field "Phased-Update-Percentage"
  assert "$(echo "$OUTPUT" | jq -c .excluded_package_metadata_fields)" == \
    '["Phased-Update-Percentage"]'
else
  expect_succ pulp deb publication create \
    --repository "${ENTITIES_NAME}_repo" \
    --simple
fi

PUBLICATION_HREF=$(echo "$OUTPUT" | jq -r .pulp_href)

expect_succ pulp deb distribution create --name "${ENTITIES_NAME}_distro" \
  --base-path "cli_test_deb_distro" \
  --publication "$PUBLICATION_HREF"

expect_succ pulp deb distribution destroy --name "${ENTITIES_NAME}_distro"
expect_succ pulp deb publication  destroy --href "${PUBLICATION_HREF}"
expect_succ pulp deb repository   destroy --name "${ENTITIES_NAME}_repo"
expect_succ pulp deb remote       destroy --name "${ENTITIES_NAME}_remote"
