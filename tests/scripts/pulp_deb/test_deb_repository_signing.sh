#!/bin/bash

set -eu

# shellcheck source=tests/scripts/config.source
. "$(dirname "$(dirname "$(realpath "$0")")")/config.source"

ENTITIES_NAME="test_deb_repository_signing"

cleanup() {
  pulp deb repository destroy --name "${ENTITIES_NAME}_repo" || true
}
trap cleanup EXIT

# Check .ci/container_setup.d/10-install-signing-service.sh on how to setup the
# signing service
expect_succ pulp signing-service list
expect_succ test "$(echo "$OUTPUT" | jq -r length)" -ge "1"
expect_succ pulp signing-service show --name "sign_deb_release"
signing_service_href=$(echo "$OUTPUT" | jq -r '.pulp_href')

# Test repository creation without signing service (baseline)
expect_succ pulp deb repository create \
  --name "${ENTITIES_NAME}_repo"
expect_succ pulp deb repository show --name "${ENTITIES_NAME}_repo"
assert "$(echo "$OUTPUT" | jq -r .signing_service)" == "null"
assert "$(echo "$OUTPUT" | jq -r .signing_service_release_overrides)" == "{}"

cleanup

# Test repository creation with signing service
expect_succ pulp deb repository create \
  --name "${ENTITIES_NAME}_repo" \
  --signing-service "sign_deb_release"
expect_succ pulp deb repository show --name "${ENTITIES_NAME}_repo"
assert "$(echo "$OUTPUT" | jq -r .signing_service)" = "${signing_service_href}"
assert "$(echo "$OUTPUT" | jq -r .signing_service_release_overrides)" = "{}"

cleanup

# Test --signing-service-release-overrides validation: must be in distribution=pulp_href format
expect_fail pulp deb repository create \
  --name "${ENTITIES_NAME}_repo" \
  --signing-service-release-overrides "invalid_format"
assert "${ERROUTPUT}" =~ "must be in the format 'distribution=pulp_href'"

# Test --signing-service-release-overrides validation - valid format
expect_succ pulp deb repository create \
  --name "${ENTITIES_NAME}_repo" \
  --signing-service-release-overrides "jammy=${signing_service_href}"
expect_succ pulp deb repository show --name "${ENTITIES_NAME}_repo"
assert "$(echo "$OUTPUT" | jq -r .signing_service)" == "null"
assert "$(echo "$OUTPUT" | jq -r .signing_service_release_overrides.jammy)" == "${signing_service_href}"

cleanup
