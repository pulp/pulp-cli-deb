
LANGUAGES=de
GLUE_PLUGINS=$(notdir $(wildcard pulp-glue-deb/pulp_glue/*))
CLI_PLUGINS=$(notdir $(wildcard pulpcore/cli/*))

info:
	@echo Pulp glue
	@echo plugins: $(GLUE_PLUGINS)
	@echo Pulp CLI
	@echo plugins: $(CLI_PLUGINS)

build:
	cd pulp-glue-deb; pyproject-build -n
	pyproject-build -n

black: format

format:
	isort .
	cd pulp-glue-deb; isort .
	black .

lint:
	find tests .ci -name '*.sh' -print0 | xargs -0 shellcheck -x
	isort -c --diff .
	cd pulp-glue-deb; isort -c --diff .
	black --diff --check .
	flake8
	.ci/scripts/check_cli_dependencies.py
	.ci/scripts/check_click_for_mypy.py
	MYPYPATH=pulp-glue-deb mypy
	cd pulp-glue-deb; mypy
	@echo "🙊 Code 🙈 LGTM 🙉 !"

tests/cli.toml:
	cp $@.example $@
	@echo "In order to configure the tests to talk to your test server, you might need to edit $@ ."

test: | tests/cli.toml
	python3 -m pytest -v tests pulp-glue-deb/tests

livetest: | tests/cli.toml
	python3 -m pytest -v tests pulp-glue-deb/tests -m live

unittest:
	python3 -m pytest -v tests pulp-glue-deb/tests -m "not live"

unittest_glue:
	python3 -m pytest -v pulp-glue-deb/tests -m "not live"

pulp-glue-deb/pulp_glue/%/locale/messages.pot: pulp-glue-deb/pulp_glue/%/*.py
	xgettext -d $* -o $@ pulp-glue-deb/pulp_glue/$*/*.py
	sed -i 's/charset=CHARSET/charset=UTF-8/g' $@

pulpcore/cli/%/locale/messages.pot: pulpcore/cli/%/*.py
	xgettext -d $* -o $@ pulpcore/cli/$*/*.py
	sed -i 's/charset=CHARSET/charset=UTF-8/g' $@

extract_messages: $(foreach GLUE_PLUGIN,$(GLUE_PLUGINS),pulp-glue-deb/pulp_glue/$(GLUE_PLUGIN)/locale/messages.pot) $(foreach CLI_PLUGIN,$(CLI_PLUGINS),pulpcore/cli/$(CLI_PLUGIN)/locale/messages.pot)

$(foreach LANGUAGE,$(LANGUAGES),pulp-glue-deb/pulp_glue/%/locale/$(LANGUAGE)/LC_MESSAGES/messages.po): pulp-glue-deb/pulp_glue/%/locale/messages.pot
	[ -e $(@D) ] || mkdir -p $(@D)
	[ ! -e $@ ] || msgmerge --update $@ $<
	[ -e $@ ] || cp $< $@

$(foreach LANGUAGE,$(LANGUAGES),pulpcore/cli/%/locale/$(LANGUAGE)/LC_MESSAGES/messages.po): pulpcore/cli/%/locale/messages.pot
	[ -e $(@D) ] || mkdir -p $(@D)
	[ ! -e $@ ] || msgmerge --update $@ $<
	[ -e $@ ] || cp $< $@

%.mo: %.po
	msgfmt -o $@ $<

compile_messages: $(foreach LANGUAGE,$(LANGUAGES),$(foreach GLUE_PLUGIN,$(GLUE_PLUGINS),pulp-glue-deb/pulp_glue/$(GLUE_PLUGIN)/locale/$(LANGUAGE)/LC_MESSAGES/messages.mo)) $(foreach LANGUAGE,$(LANGUAGES),$(foreach CLI_PLUGIN,$(CLI_PLUGINS),pulpcore/cli/$(CLI_PLUGIN)/locale/$(LANGUAGE)/LC_MESSAGES/messages.mo))
.PHONY: build info black lint test
.PRECIOUS: $(foreach LANGUAGE,$(LANGUAGES),$(foreach GLUE_PLUGIN,$(GLUE_PLUGINS),pulp-glue-deb/pulp_glue/$(GLUE_PLUGIN)/locale/$(LANGUAGE)/LC_MESSAGES/messages.po)) $(foreach LANGUAGE,$(LANGUAGES),$(foreach CLI_PLUGIN,$(CLI_PLUGINS),pulpcore/cli/$(CLI_PLUGIN)/locale/$(LANGUAGE)/LC_MESSAGES/messages.po))
