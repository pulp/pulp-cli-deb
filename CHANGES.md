# Changelog

[//]: # (You should *NOT* be adding new change log entries to this file, this)
[//]: # (file is managed by towncrier. You *may* edit previous change logs to)
[//]: # (fix problems like typo corrections or such.)
[//]: # (To add a new change log entry, please see)
[//]: # (https://docs.pulpproject.org/contributing/git.html#changelog-update)

[//]: # (WARNING: Don't drop the towncrier directive!)

[//]: # (towncrier release notes start)

## 0.3.2 (2025-02-26) {: #0.3.2 }



No significant changes.


### Pulp-deb GLUE {: #0.3.2-pulp-deb-glue }


No significant changes.


---

## 0.3.1 (2025-01-22) {: #0.3.1 }



No significant changes.


### Pulp-deb GLUE {: #0.3.1-pulp-deb-glue }


No significant changes.


---

## 0.3.0 (2024-10-02) {: #0.3.0 }



#### Features {: #0.3.0-feature }

- Bump dependency on pulp-cli up to version 0.29.*.
  [#138](https://github.com/pulp/pulp-cli-deb/issues/138)


### Pulp-deb GLUE {: #0.3.0-pulp-deb-glue }


#### Features {: #0.3.0-pulp-deb-glue-feature }

- Bump dependency on pulp-glue up to version 0.29.*.
  [#138](https://github.com/pulp/pulp-cli-deb/issues/138)


---

## 0.2.0 (2024-08-06) {: #0.2.0 }



#### Features {: #0.2.0-feature }

- Bump dependency on pulp-cli up to version 0.27.*.
  [#127](https://github.com/pulp/pulp-cli-deb/issues/127)


### Pulp-deb GLUE {: #0.2.0-pulp-deb-glue }


#### Features {: #0.2.0-pulp-deb-glue-feature }

- Bump dependency on pulp-glue up to version 0.27.*.
  [#127](https://github.com/pulp/pulp-cli-deb/issues/127)


---

## 0.1.0 (2024-05-06) {: #0.1.0 }



#### Features {: #0.1.0-feature }

- Added `gpgkey` option to the remote command.
  [#108](https://github.com/pulp/pulp-cli-deb/issues/108)
- Installation with Pulp CLI 0.25 is now supported.
  [#114](https://github.com/pulp/pulp-cli-deb/issues/114)
- Added the create command for content of type release_component.
  [#118](https://github.com/pulp/pulp-cli-deb/issues/118)


#### Deprecations and Removals {: #0.1.0-removal }

- Pulp CLI deb now requires at least Pulp CLI >=0.23.2 to run.
  [#114](https://github.com/pulp/pulp-cli-deb/issues/114)
- Dropped support for python < 3.8.


### Pulp-deb GLUE {: #0.1.0-pulp-deb-glue }


#### Deprecations and Removals {: #0.1.0-pulp-deb-glue-removal }

- Dropped support for python < 3.8.


---

## 0.0.7 (2024-02-19)


No significant changes.


### Pulp GLUE deb


No significant changes.


---


## 0.0.6 (2024-02-19)


#### Features

- Modernized the build process with setuptools to use `pyproject.toml` instead of `setup.py`.


### Pulp GLUE deb


#### Features

- The pulp-glue-deb library layer is now available as a separate package.
  [#65](https://github.com/pulp/pulp-cli-deb/issues/65)


## 0.0.5 (2023-09-05)


### Features

- Added new ``content`` command for showing deb content and uploading debian packages.
  [#23](https://github.com/pulp/pulp-cli-deb/issues/23)


### Bugfixes

- Added ``--no-structured`` flag to the ``publication create`` command, so the new default value of "structured" can be overridden for ``pulp_deb>=3.0.0``.
  [#66](https://github.com/pulp/pulp-cli-deb/issues/66)


---


## 0.0.4 (2023-03-09)


### Misc

- Adopted PREFIX_ID pattern introduced in pulp-cli 0.14.
  [#27](https://github.com/pulp/pulp-cli-deb/issues/27)


---


## 0.0.3 (2023-01-03)


### Features

- Added support for the new --optimize/--no-optimize sync option.
  [#31](https://github.com/pulp/pulp-cli-deb/issues/31)
- Use flags for ``--simple`` and ``--structured`` on publication create instead of having users
  specify a value of ``True``.
  [#36](https://github.com/pulp/pulp-cli-deb/issues/36)


### Improved Documentation

- Added a help text for the --mirror/--no-mirror sync option.
  [#30](https://github.com/pulp/pulp-cli-deb/issues/30)


### Deprecations and Removals

- Bumped pulp-cli dependency to >=0.13.0.
  [#10](https://github.com/pulp/pulp-cli-deb/issues/10)


### Translations

- Added rudimentary German translations files.
  [#10](https://github.com/pulp/pulp-cli-deb/issues/10)


### Misc

- [#10](https://github.com/pulp/pulp-cli-deb/issues/10)


---


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
