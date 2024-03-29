##############################################################################
# THIS FILE IS GENERATED BY MXMAKE
#
# DOMAINS:
#: applications.cookiecutter
#: applications.zest-releaser
#: applications.zope
#: core.base
#: core.mxenv
#: core.mxfiles
#: core.packages
#: qa.black
#: qa.coverage
#: qa.isort
#: qa.test
#: qa.zpretty
#
# SETTINGS (ALL CHANGES MADE BELOW SETTINGS WILL BE LOST)
##############################################################################

## core.base

# `deploy` target dependencies.
# No default value.
DEPLOY_TARGETS?=

# target to be executed when calling `make run`
# No default value.
RUN_TARGET?=

# Additional files and folders to remove when running clean target
# No default value.
CLEAN_FS?=

# Optional makefile to include before default targets. This can
# be used to provide custom targets or hook up to existing targets.
# Default: include.mk
INCLUDE_MAKEFILE?=include.mk

## core.mxenv

# Python interpreter to use.
# Default: python3
PYTHON_BIN?=python3

# Minimum required Python version.
# Default: 3.7
PYTHON_MIN_VERSION?=3.7

# Flag whether to use virtual environment. If `false`, the
# interpreter according to `PYTHON_BIN` found in `PATH` is used.
# Default: true
VENV_ENABLED?=true

# Flag whether to create a virtual environment. If set to `false`
# and `VENV_ENABLED` is `true`, `VENV_FOLDER` is expected to point to an
# existing virtual environment.
# Default: true
VENV_CREATE?=true

# The folder of the virtual environment.
# If `VENV_ENABLED` is `true` and `VENV_CREATE` is true it is used as the
# target folder for the virtual environment. If `VENV_ENABLED` is `true` and
# `VENV_CREATE` is false it is expected to point to an existing virtual
# environment. If `VENV_ENABLED` is `false` it is ignored.
# Default: venv
VENV_FOLDER?=venv

# mxdev to install in virtual environment.
# Default: mxdev
MXDEV?=mxdev

# mxmake to install in virtual environment.
# Default: mxmake
MXMAKE?=mxmake

## qa.zpretty

# Source folder to scan for XML and ZCML files.
# Default: src
ZPRETTY_SRC?=src

## qa.isort

# Source folder to scan for Python files to run isort on.
# Default: src
ISORT_SRC?=src

## qa.black

# Source folder to scan for Python files to run black on.
# Default: src
BLACK_SRC?=src

## core.mxfiles

# The config file to use.
# Default: mx.ini
PROJECT_CONFIG?=mx.ini

## qa.test

# The command which gets executed. Defaults to the location the
# :ref:`run-tests` template gets rendered to if configured.
# Default: .mxmake/files/run-tests.sh
TEST_COMMAND?=.mxmake/files/run-tests.sh

# Additional Python requirements for running tests to be
# installed (via pip).
# Default: pytest
TEST_REQUIREMENTS?=pytest

# Additional make targets the test target depends on.
# No default value.
TEST_DEPENDENCY_TARGETS?=

## qa.coverage

# The command which gets executed. Defaults to the location the
# :ref:`run-coverage` template gets rendered to if configured.
# Default: .mxmake/files/run-coverage.sh
COVERAGE_COMMAND?=.mxmake/files/run-coverage.sh

## applications.zope

# cookiecutter configuration file to use
# Default: instance.yaml
ZOPE_CONFIGURATION_FILE?=instance.yaml

# cookiecutter configuration file to use
# Default: https://github.com/plone/cookiecutter-zope-instance
ZOPE_TEMPLATE?=https://github.com/plone/cookiecutter-zope-instance

# The Zope folder "instance" will be generated relative to this existing folder.
# Default: .
ZOPE_BASE_FOLDER?=.

# script to run
# Default: No Default
ZOPE_SCRIPTNAME?=No Default

##############################################################################
# END SETTINGS - DO NOT EDIT BELOW THIS LINE
##############################################################################

INSTALL_TARGETS?=
DIRTY_TARGETS?=
CLEAN_TARGETS?=
PURGE_TARGETS?=
CHECK_TARGETS?=
FORMAT_TARGETS?=

# Defensive settings for make: https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
# for Makefile debugging purposes add -x to the .SHELLFLAGS
.SHELLFLAGS:=-eu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# mxmake folder
MXMAKE_FOLDER?=.mxmake

# Sentinel files
SENTINEL_FOLDER?=$(MXMAKE_FOLDER)/sentinels
SENTINEL?=$(SENTINEL_FOLDER)/about.txt
$(SENTINEL):
	@mkdir -p $(SENTINEL_FOLDER)
	@echo "Sentinels for the Makefile process." > $(SENTINEL)

##############################################################################
# mxenv
##############################################################################

# Check if given Python is installed
ifeq (,$(shell which $(PYTHON_BIN)))
$(error "PYTHON=$(PYTHON_BIN) not found in $(PATH)")
endif

# Check if given Python version is ok
PYTHON_VERSION_OK=$(shell $(PYTHON_BIN) -c "import sys; print((int(sys.version_info[0]), int(sys.version_info[1])) >= tuple(map(int, '$(PYTHON_MIN_VERSION)'.split('.'))))")
ifeq ($(PYTHON_VERSION_OK),0)
$(error "Need Python >= $(PYTHON_MIN_VERSION)")
endif

# Check if venv folder is configured if venv is enabled
ifeq ($(shell [[ "$(VENV_ENABLED)" == "true" && "$(VENV_FOLDER)" == "" ]] && echo "true"),"true")
$(error "VENV_FOLDER must be configured if VENV_ENABLED is true")
endif

# determine the executable path
ifeq ("$(VENV_ENABLED)", "true")
MXENV_PATH=$(VENV_FOLDER)/bin/
else
MXENV_PATH=
endif

MXENV_TARGET:=$(SENTINEL_FOLDER)/mxenv.sentinel
$(MXENV_TARGET): $(SENTINEL)
ifeq ("$(VENV_ENABLED)", "true")
	@echo "Setup Python Virtual Environment under '$(VENV_FOLDER)'"
	@$(PYTHON_BIN) -m venv $(VENV_FOLDER)
endif
	@$(MXENV_PATH)pip install -U pip setuptools wheel
	@$(MXENV_PATH)pip install -U $(MXDEV)
	@$(MXENV_PATH)pip install -U $(MXMAKE)
	@touch $(MXENV_TARGET)

.PHONY: mxenv
mxenv: $(MXENV_TARGET)

.PHONY: mxenv-dirty
mxenv-dirty:
	@rm -f $(MXENV_TARGET)

.PHONY: mxenv-clean
mxenv-clean: mxenv-dirty
ifeq ("$(VENV_ENABLED)", "true")
	@rm -rf $(VENV_FOLDER)
else
	@$(MXENV_PATH)pip uninstall -y $(MXDEV)
	@$(MXENV_PATH)pip uninstall -y $(MXMAKE)
endif

INSTALL_TARGETS+=mxenv
DIRTY_TARGETS+=mxenv-dirty
CLEAN_TARGETS+=mxenv-clean

##############################################################################
# zpretty
##############################################################################

ZPRETTY_TARGET:=$(SENTINEL_FOLDER)/zpretty.sentinel
$(ZPRETTY_TARGET): $(MXENV_TARGET)
	@echo "Install zpretty"
	@$(MXENV_PATH)pip install zpretty
	@touch $(ZPRETTY_TARGET)

.PHONY: zpretty-check
zpretty-check: $(ZPRETTY_TARGET)
	@echo "Run zpretty check in: $(ZPRETTY_SRC)"
	@find $(ZPRETTY_SRC) -name '*.zcml' -or -name '*.xml' -exec $(MXENV_PATH)zpretty --check {} +

.PHONY: zpretty-format
zpretty-format: $(ZPRETTY_TARGET)
	@echo "Run zpretty format in: $(ZPRETTY_SRC)"
	@find $(ZPRETTY_SRC) -name '*.zcml' -or -name '*.xml' -exec $(MXENV_PATH)zpretty -i {} +

.PHONY: zpretty-dirty
zpretty-dirty:
	@rm -f $(ZPRETTY_TARGET)

.PHONY: zpretty-clean
zpretty-clean: zpretty-dirty
	@test -e $(MXENV_PATH)pip && $(MXENV_PATH)pip uninstall -y zpretty || :

INSTALL_TARGETS+=$(ZPRETTY_TARGET)
CHECK_TARGETS+=zpretty-check
FORMAT_TARGETS+=zpretty-format
DIRTY_TARGETS+=zpretty-dirty
CLEAN_TARGETS+=zpretty-clean

##############################################################################
# isort
##############################################################################

ISORT_TARGET:=$(SENTINEL_FOLDER)/isort.sentinel
$(ISORT_TARGET): $(MXENV_TARGET)
	@echo "Install isort"
	@$(MXENV_PATH)pip install isort
	@touch $(ISORT_TARGET)

.PHONY: isort-check
isort-check: $(ISORT_TARGET)
	@echo "Run isort check"
	@$(MXENV_PATH)isort --check $(ISORT_SRC)

.PHONY: isort-format
isort-format: $(ISORT_TARGET)
	@echo "Run isort format"
	@$(MXENV_PATH)isort $(ISORT_SRC)

.PHONY: isort-dirty
isort-dirty:
	@rm -f $(ISORT_TARGET)

.PHONY: isort-clean
isort-clean: isort-dirty
	@test -e $(MXENV_PATH)pip && $(MXENV_PATH)pip uninstall -y isort || :

INSTALL_TARGETS+=$(ISORT_TARGET)
CHECK_TARGETS+=isort-check
FORMAT_TARGETS+=isort-format
DIRTY_TARGETS+=isort-dirty
CLEAN_TARGETS+=isort-clean

##############################################################################
# black
##############################################################################

BLACK_TARGET:=$(SENTINEL_FOLDER)/black.sentinel
$(BLACK_TARGET): $(MXENV_TARGET)
	@echo "Install Black"
	@$(MXENV_PATH)pip install black
	@touch $(BLACK_TARGET)

.PHONY: black-check
black-check: $(BLACK_TARGET)
	@echo "Run black checks"
	@$(MXENV_PATH)black --check $(BLACK_SRC)

.PHONY: black-format
black-format: $(BLACK_TARGET)
	@echo "Run black format"
	@$(MXENV_PATH)black $(BLACK_SRC)

.PHONY: black-dirty
black-dirty:
	@rm -f $(BLACK_TARGET)

.PHONY: black-clean
black-clean: black-dirty
	@test -e $(MXENV_PATH)pip && $(MXENV_PATH)pip uninstall -y black || :

INSTALL_TARGETS+=$(BLACK_TARGET)
CHECK_TARGETS+=black-check
FORMAT_TARGETS+=black-format
DIRTY_TARGETS+=black-dirty
CLEAN_TARGETS+=black-clean

##############################################################################
# mxfiles
##############################################################################

# case `core.sources` domain not included
SOURCES_TARGET?=

# File generation target
MXMAKE_FILES?=$(MXMAKE_FOLDER)/files

# set environment variables for mxmake
define set_mxfiles_env
	@export MXMAKE_MXENV_PATH=$(1)
	@export MXMAKE_FILES=$(2)
endef

# unset environment variables for mxmake
define unset_mxfiles_env
	@unset MXMAKE_MXENV_PATH
	@unset MXMAKE_FILES
endef

$(PROJECT_CONFIG):
ifneq ("$(wildcard $(PROJECT_CONFIG))","")
	@touch $(PROJECT_CONFIG)
else
	@echo "[settings]" > $(PROJECT_CONFIG)
endif

LOCAL_PACKAGE_FILES:=$(wildcard pyproject.toml setup.cfg setup.py requirements.txt constraints.txt)

FILES_TARGET:=requirements-mxdev.txt
$(FILES_TARGET): $(PROJECT_CONFIG) $(MXENV_TARGET) $(SOURCES_TARGET) $(LOCAL_PACKAGE_FILES)
	@echo "Create project files"
	@mkdir -p $(MXMAKE_FILES)
	$(call set_mxfiles_env,$(MXENV_PATH),$(MXMAKE_FILES))
	@$(MXENV_PATH)mxdev -n -c $(PROJECT_CONFIG)
	$(call unset_mxfiles_env,$(MXENV_PATH),$(MXMAKE_FILES))
	@touch $(FILES_TARGET)

.PHONY: mxfiles
mxfiles: $(FILES_TARGET)

.PHONY: mxfiles-dirty
mxfiles-dirty:
	@touch $(PROJECT_CONFIG)

.PHONY: mxfiles-clean
mxfiles-clean: mxfiles-dirty
	@rm -rf constraints-mxdev.txt requirements-mxdev.txt $(MXMAKE_FILES)

INSTALL_TARGETS+=mxfiles
DIRTY_TARGETS+=mxfiles-dirty
CLEAN_TARGETS+=mxfiles-clean

##############################################################################
# packages
##############################################################################

# additional sources targets which requires package re-install on change
-include $(MXMAKE_FILES)/additional_sources_targets.mk
ADDITIONAL_SOURCES_TARGETS?=

INSTALLED_PACKAGES=$(MXMAKE_FILES)/installed.txt

PACKAGES_TARGET:=$(INSTALLED_PACKAGES)
$(PACKAGES_TARGET): $(FILES_TARGET) $(ADDITIONAL_SOURCES_TARGETS)
	@echo "Install python packages"
	@$(MXENV_PATH)pip install -r $(FILES_TARGET)
	@$(MXENV_PATH)pip freeze > $(INSTALLED_PACKAGES)
	@touch $(PACKAGES_TARGET)

.PHONY: packages
packages: $(PACKAGES_TARGET)

.PHONY: packages-dirty
packages-dirty:
	@rm -f $(PACKAGES_TARGET)

.PHONY: packages-clean
packages-clean:
	@test -e $(FILES_TARGET) \
		&& test -e $(MXENV_PATH)pip \
		&& $(MXENV_PATH)pip uninstall -y -r $(FILES_TARGET) \
		|| :
	@rm -f $(PACKAGES_TARGET)

INSTALL_TARGETS+=packages
DIRTY_TARGETS+=packages-dirty
CLEAN_TARGETS+=packages-clean

##############################################################################
# test
##############################################################################

TEST_TARGET:=$(SENTINEL_FOLDER)/test.sentinel
$(TEST_TARGET): $(MXENV_TARGET)
	@echo "Install $(TEST_REQUIREMENTS)"
	@$(MXENV_PATH)pip install $(TEST_REQUIREMENTS)
	@touch $(TEST_TARGET)

.PHONY: test
test: $(FILES_TARGET) $(SOURCES_TARGET) $(PACKAGES_TARGET) $(TEST_TARGET) $(TEST_DEPENDENCY_TARGETS)
	@echo "Run tests"
	@test -z "$(TEST_COMMAND)" && echo "No test command defined"
	@test -z "$(TEST_COMMAND)" || bash -c "$(TEST_COMMAND)"

.PHONY: test-dirty
test-dirty:
	@rm -f $(TEST_TARGET)

.PHONY: test-clean
test-clean: test-dirty
	@test -e $(MXENV_PATH)pip && $(MXENV_PATH)pip uninstall -y $(TEST_REQUIREMENTS) || :
	@rm -rf .pytest_cache

INSTALL_TARGETS+=$(TEST_TARGET)
CLEAN_TARGETS+=test-clean
DIRTY_TARGETS+=test-dirty

##############################################################################
# coverage
##############################################################################

COVERAGE_TARGET:=$(SENTINEL_FOLDER)/coverage.sentinel
$(COVERAGE_TARGET): $(TEST_TARGET)
	@echo "Install Coverage"
	@$(MXENV_PATH)pip install -U coverage
	@touch $(COVERAGE_TARGET)

.PHONY: coverage
coverage: $(FILES_TARGET) $(SOURCES_TARGET) $(PACKAGES_TARGET) $(COVERAGE_TARGET)
	@echo "Run coverage"
	@test -z "$(COVERAGE_COMMAND)" && echo "No coverage command defined"
	@test -z "$(COVERAGE_COMMAND)" || bash -c "$(COVERAGE_COMMAND)"

.PHONY: coverage-dirty
coverage-dirty:
	@rm -f $(COVERAGE_TARGET)

.PHONY: coverage-clean
coverage-clean: coverage-dirty
	@test -e $(MXENV_PATH)pip && $(MXENV_PATH)pip uninstall -y coverage || :
	@rm -rf .coverage htmlcov

INSTALL_TARGETS+=$(COVERAGE_TARGET)
DIRTY_TARGETS+=coverage-dirty
CLEAN_TARGETS+=coverage-clean

##############################################################################
# cookiecutter
##############################################################################

COOKIECUTTER_TARGET:=$(SENTINEL_FOLDER)/cookiecutter.sentinel
$(COOKIECUTTER_TARGET): $(MXENV_TARGET)
	@echo "Install cookiecutter"
	@$(MXENV_PATH)pip install "cookiecutter>=2.1.1"
	@touch $(COOKIECUTTER_TARGET)

.PHONY: cookiecutter-dirty
cookiecutter-dirty:
	@rm -f $(COOKIECUTTER_TARGET)

.PHONY: cookiecutter-clean
cookiecutter-clean: cookiecutter-dirty
	@test -e $(MXENV_PATH)pip && $(MXENV_PATH)pip uninstall -y cookiecutter || :
	@rm -f $(COOKIECUTTER_TARGET)

DIRTY_TARGETS+=cookiecutter-dirty
CLEAN_TARGETS+=cookiecutter-clean

##############################################################################
# zope
##############################################################################

ZOPE_INSTANCE_FOLDER:=$(ZOPE_BASE_FOLDER)/instance
ZOPE_INSTANCE_TARGET:=$(ZOPE_INSTANCE_FOLDER)/etc/zope.ini $(ZOPE_INSTANCE_FOLDER)/etc/zope.conf $(ZOPE_INSTANCE_FOLDER)/etc/site.zcml

${ZOPE_CONFIGURATION_FILE}:
	@touch ${ZOPE_CONFIGURATION_FILE}

$(ZOPE_INSTANCE_TARGET): $(COOKIECUTTER_TARGET) $(ZOPE_CONFIGURATION_FILE)
	@echo Create Plone/Zope configuration from $(ZOPE_TEMPLATE) to $(ZOPE_INSTANCE_FOLDER)
	@$(MXENV_PATH)cookiecutter -f --no-input --config-file $(ZOPE_CONFIGURATION_FILE) --output-dir $(ZOPE_BASE_FOLDER) $(ZOPE_TEMPLATE)

.PHONY: zope-instance
zope-instance: $(ZOPE_INSTANCE_TARGET) $(SOURCES)

.PHONY: zope-start
zope-start: $(ZOPE_INSTANCE_TARGET) $(PACKAGES_TARGET)
	@echo "Start Zope/Plone with configuration in $(ZOPE_INSTANCE_FOLDER)"
	@$(MXENV_PATH)runwsgi -v "$(ZOPE_INSTANCE_FOLDER)/etc/zope.ini"

.PHONY: zope-debug
zope-debug: $(ZOPE_INSTANCE_TARGET) $(PACKAGES_TARGET)
	@echo "Start Zope/Plone with configuration in $(ZOPE_INSTANCE_FOLDER)"
	@$(MXENV_PATH)zconsole debug "$(ZOPE_INSTANCE_FOLDER)/etc/zope.ini"

.PHONY: zope-runscript
zope-runscript: $(ZOPE_INSTANCE_TARGET) $(PACKAGES_TARGET)
	@echo "Run Zope/Plone Console Script $(ZOPE_SCRIPTNAME) in $(ZOPE_INSTANCE_FOLDER)"
	@$(MXENV_PATH)zconsole run "$(ZOPE_INSTANCE_FOLDER)/etc/zope.ini" $(ZOPE_SCRIPTNAME)

.PHONY: zope-dirty
zope-dirty:
	@touch ${ZOPE_CONFIGURATION_FILE}

.PHONY: zope-clean
zope-clean:
	@touch ${ZOPE_CONFIGURATION_FILE}
	@rm -rf $(ZOPE_INSTANCE_FOLDER)/etc $(ZOPE_INSTANCE_FOLDER)/inituser

.PHONY: zope-purge
zope-purge: zope-dirty
	@rm -rf $(ZOPE_INSTANCE_FOLDER)

INSTALL_TARGETS+=zope-instance
DIRTY_TARGETS+=zope-dirty
CLEAN_TARGETS+=zope-clean

##############################################################################
# zest-releaser
##############################################################################

ZEST_RELEASER_TARGET:=$(SENTINEL_FOLDER)/zest-releaser.sentinel
$(ZEST_RELEASER_TARGET): $(MXENV_TARGET)
	@echo "Install zest.releaser"
	@$(MXENV_PATH)pip install zest.releaser
	@touch $(ZEST_RELEASER_TARGET)

.PHONY: zest-releaser-prerelease
zest-releaser-prerelease: $(ZEST_RELEASER_TARGET)
	@echo "Run prerelease"
	@$(MXENV_PATH)prerelease

.PHONY: zest-releaser-release
zest-releaser-release: $(ZEST_RELEASER_TARGET)
	@echo "Run release"
	@$(MXENV_PATH)release

.PHONY: zest-releaser-postrelease
zest-releaser-postrelease: $(ZEST_RELEASER_TARGET)
	@echo "Run postrelease"
	@$(MXENV_PATH)postrelease

.PHONY: zest-releaser-fullrelease
zest-releaser-fullrelease: $(ZEST_RELEASER_TARGET)
	@echo "Run fullrelease"
	@$(MXENV_PATH)fullrelease

.PHONY: zest-releaser-dirty
zest-releaser-dirty:
	@rm -f $(ZEST_RELEASER_TARGET)

.PHONY: zest-releaser-clean
zest-releaser-clean: zest-releaser-dirty
	@test -e $(MXENV_PATH)pip && $(MXENV_PATH)pip uninstall -y zest.releaser || :

INSTALL_TARGETS+=$(ZEST_RELEASER_TARGET)
DIRTY_TARGETS+=zest-releaser-dirty
CLEAN_TARGETS+=zest-releaser-clean

-include $(INCLUDE_MAKEFILE)

##############################################################################
# Default targets
##############################################################################

INSTALL_TARGET:=$(SENTINEL_FOLDER)/install.sentinel
$(INSTALL_TARGET): $(INSTALL_TARGETS)
	@touch $(INSTALL_TARGET)

.PHONY: install
install: $(INSTALL_TARGET)
	@touch $(INSTALL_TARGET)

.PHONY: run
run: $(RUN_TARGET)

.PHONY: deploy
deploy: $(DEPLOY_TARGETS)

.PHONY: dirty
dirty: $(DIRTY_TARGETS)
	@rm -f $(INSTALL_TARGET)

.PHONY: clean
clean: dirty $(CLEAN_TARGETS)
	@rm -rf $(CLEAN_TARGETS) $(MXMAKE_FOLDER) $(CLEAN_FS)

.PHONY: purge
purge: clean $(PURGE_TARGETS)

.PHONY: runtime-clean
runtime-clean:
	@echo "Remove runtime artifacts, like byte-code and caches."
	@find . -name '*.py[c|o]' -delete
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

.PHONY: check
check: $(CHECK_TARGETS)

.PHONY: format
format: $(FORMAT_TARGETS)
