#!/bin/sh

# shellcheck source=tests/scripts/config.source
. "$(dirname "$(dirname "$(realpath "$0")")")/config.source"

cleanup() {
  pulp deb remote destroy --name "cli_test_deb_remote" || true
  pulp deb repository destroy --name "cli_test_deb_repository" || true
  pulp deb distribution destroy --name "cli_test_deb_distro" || true
}
trap cleanup EXIT

if [ "$VERIFY_SSL" = "false" ]
then
  curl_opt="-k"
else
  curl_opt=""
fi

expect_succ pulp deb remote create --name "cli_test_deb_remote" --url "$DEB_REMOTE_URL" --distribution "$DEB_DISTRIBUTION"
expect_succ pulp deb repository create --name "cli_test_deb_repository"

expect_succ pulp deb repository sync --name "cli_test_deb_repository" --remote "cli_test_deb_remote"
expect_succ pulp deb publication create --repository "cli_test_deb_repository" --simple "True"
PUBLICATION_HREF=$(echo "$OUTPUT" | jq -r .pulp_href)

expect_succ pulp deb distribution create --name "cli_test_deb_distro" \
  --base-path "cli_test_deb_distro" \
  --publication "$PUBLICATION_HREF"

expect_succ curl "$curl_opt" --head --fail "$PULP_BASE_URL/pulp/content/cli_test_deb_distro/dists/default/Release"

expect_succ pulp deb distribution destroy --name "cli_test_deb_distro"
expect_succ pulp deb publication destroy --href "$PUBLICATION_HREF"

expect_succ pulp deb repository destroy --name "cli_test_deb_repository"
expect_succ pulp deb remote destroy --name "cli_test_deb_remote"
