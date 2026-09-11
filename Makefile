.PHONY: setup doctor test
PYTHON ?= python3
setup:
	$(PYTHON) -c "import sys; assert sys.version_info >= (3, 11), 'Python 3.11+ required'; print('PASS setup: standard-library starter, no packages required')"
doctor: setup
test:
	$(PYTHON) -c "import json; c=json.load(open('contracts/mac-v0.json')); assert c['id']=='siliconbadgers.mac.v0'; assert len(c['vector_columns'])==5; print('PASS MAC contract structure (not RTL verification)')"
