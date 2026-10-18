.PHONY: setup doctor test
UV ?= uv
PROJECT_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PYTHON ?= python3
RUN_PYTHON = $(UV) run --locked --project "$(PROJECT_ROOT)" $(PYTHON)
setup:
	$(UV) sync --locked --project "$(PROJECT_ROOT)"
	$(RUN_PYTHON) -c "import sys; assert sys.version_info >= (3, 11), 'Python 3.11+ required'; print('PASS setup: standard-library starter, no packages required')"
doctor: setup
test:
	$(RUN_PYTHON) -c "import json; c=json.load(open('contracts/mac-v0.json')); assert c['id']=='siliconbadgers.mac.v0'; assert len(c['vector_columns'])==5; print('PASS MAC contract structure (not RTL verification)')"
