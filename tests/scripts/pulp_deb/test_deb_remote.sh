#!/bin/bash

# shellcheck source=tests/scripts/config.source
. "$(dirname "$(dirname "$(realpath "$0")")")/config.source"

ENTITIES_NAME="test_deb_remote"

cleanup() {
  pulp deb remote destroy --name "${ENTITIES_NAME}" || true
}
trap cleanup EXIT

# Fail to create some remotes:
expect_fail pulp deb remote create --name "foo" --url "foo" --distribution ""
expect_fail pulp deb remote create --name "foo" --url "foo"
expect_fail pulp deb remote create --name "foo" --url "" --distribution "foo"
expect_fail pulp deb remote create --name "foo" --distribution "foo"
expect_fail pulp deb remote create --name "" --url "foo" --distribution "foo"
expect_fail pulp deb remote create --url "foo" --distribution "foo"

# Create and trivially update a remote:
expect_succ pulp deb remote create --name "${ENTITIES_NAME}" \
  --url "foo" \
  --distribution "foo" \
  --component "foo" \
  --architecture "foo"

assert "$(echo "$OUTPUT" | jq -r .url)" == "foo"
assert "$(echo "$OUTPUT" | jq -r .distributions)" == "foo"
assert "$(echo "$OUTPUT" | jq -r .components)" == "foo"
assert "$(echo "$OUTPUT" | jq -r .architectures)" == "foo"
expect_succ pulp deb remote update --name "${ENTITIES_NAME}"

# Try some possible modifications of the remote's distribution:
expect_succ pulp deb remote update --name "${ENTITIES_NAME}" --distribution "bar"
expect_succ pulp deb remote show --name "${ENTITIES_NAME}"
assert "$(echo "$OUTPUT" | jq -r .distributions)" == "bar"
expect_succ pulp deb remote update --name "${ENTITIES_NAME}" --distribution "bar" --distribution "baz"
expect_succ pulp deb remote show --name "${ENTITIES_NAME}"
assert "$(echo "$OUTPUT" | jq -r .distributions)" == "bar baz"
expect_succ pulp deb remote update --name "${ENTITIES_NAME}" --distribution "bar" --distribution ""
expect_succ pulp deb remote show --name "${ENTITIES_NAME}"
assert "$(echo "$OUTPUT" | jq -r .distributions)" == "bar"
expect_fail pulp deb remote update --name "${ENTITIES_NAME}" --distribution ""
assert "${ERROUTPUT}" == 'Error: Must have at least one distribution for remote.'

# Try some possible modifications of the remote's components:
expect_succ pulp deb remote update --name "${ENTITIES_NAME}" --component "bar"
expect_succ pulp deb remote show --name "${ENTITIES_NAME}"
assert "$(echo "$OUTPUT" | jq -r .components)" == "bar"
expect_succ pulp deb remote update --name "${ENTITIES_NAME}" --component "bar" --component "baz"
expect_succ pulp deb remote show --name "${ENTITIES_NAME}"
assert "$(echo "$OUTPUT" | jq -r .components)" == "bar baz"
expect_succ pulp deb remote update --name "${ENTITIES_NAME}" --component "bar" --component ""
expect_succ pulp deb remote show --name "${ENTITIES_NAME}"
assert "$(echo "$OUTPUT" | jq -r .components)" == "bar"
expect_succ pulp deb remote update --name "${ENTITIES_NAME}" --component ""
expect_succ pulp deb remote show --name "${ENTITIES_NAME}"
assert "$(echo "$OUTPUT" | jq -r .components)" == "null"

# Try some possible modifications of the remote's architectures:
expect_succ pulp deb remote update --name "${ENTITIES_NAME}" --architecture "bar"
expect_succ pulp deb remote show --name "${ENTITIES_NAME}"
assert "$(echo "$OUTPUT" | jq -r .architectures)" == "bar"
expect_succ pulp deb remote update --name "${ENTITIES_NAME}" --architecture "bar" --architecture "baz"
expect_succ pulp deb remote show --name "${ENTITIES_NAME}"
assert "$(echo "$OUTPUT" | jq -r .architectures)" == "bar baz"
expect_succ pulp deb remote update --name "${ENTITIES_NAME}" --architecture "bar" --architecture ""
expect_succ pulp deb remote show --name "${ENTITIES_NAME}"
assert "$(echo "$OUTPUT" | jq -r .architectures)" == "bar"
expect_succ pulp deb remote update --name "${ENTITIES_NAME}" --architecture ""
expect_succ pulp deb remote show --name "${ENTITIES_NAME}"
assert "$(echo "$OUTPUT" | jq -r .architectures)" == "null"

#  test with a gpg key if cli_version >= 0.24.0
cli_version=$( pulp  --version  | awk '{print $NF}' )
if [ "$({  echo "$cli_version" ; echo "0.24.0"; } | sort -V | tail -n1)" = "$cli_version" ]
then
 expect_succ pulp deb remote update --name "${ENTITIES_NAME}" --gpgkey  "$(gpg --armor --export 'pulp-fixture-signing-key')"
 expect_succ pulp deb remote show --name "${ENTITIES_NAME}"
 assert "$(echo "$OUTPUT" | jq -r .gpgkey)" ==  "$(gpg --armor --export 'pulp-fixture-signing-key')"
fi

# Now destroy the remote
expect_succ pulp deb remote destroy --name "${ENTITIES_NAME}"
