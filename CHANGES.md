# Changelog

[//]: # (You should *NOT* be adding new change log entries to this file, this)
[//]: # (file is managed by towncrier. You *may* edit previous change logs to)
[//]: # (fix problems like typo corrections or such.)
[//]: # (To add a new change log entry, please see)
[//]: # (https://docs.pulpproject.org/contributing/git.html#changelog-update)

[//]: # (WARNING: Don't drop the towncrier directive!)

[//]: # (towncrier release notes start)

## 0.0.2 (2022-01-03)

### Features

- Added publication and distribution commands.
  [#3](https://github.com/pulp/pulp-cli-deb/issues/3)
- Added --component and --architecture flags to the remote command.
  [#4](https://github.com/pulp/pulp-cli-deb/issues/4)
- Added the --mirror and --no-mirror flags to the sync command.
  [#12](https://github.com/pulp/pulp-cli-deb/issues/12)


### Bugfixes

- Reworked the ``--distribution`` flag for the remote command. It is no longer required when updating a remote, and can now be specified multiple times (instead of a single ``--distributions`` flag).
  [#14](https://github.com/pulp/pulp-cli-deb/issues/14)


---


## 0.0.1 (2021-08-25)

Initial release.

---
