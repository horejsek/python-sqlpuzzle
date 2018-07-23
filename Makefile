.PHONY: all venv lint test doc upload clean
SHELL=/bin/bash

VENV_NAME?=venv
VENV_BIN=$(shell pwd)/${VENV_NAME}/bin

PYTHON=${VENV_BIN}/python3

all:
	@echo "make test - Run tests during development"
	@echo "make performance - Run performance test of this and other implementation"
	@echo "make doc - Make documentation"
	@echo "make clean - Get rid of scratch and byte files"

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip setuptools
	${PYTHON} -m pip install -e .[devel]
	touch $(VENV_NAME)/bin/activate

lint: venv
	${PYTHON} -m pylint sqlpuzzle

test: venv
	${PYTHON} -m pytest

doc:
	cd docs; make

upload: venv
	${PYTHON} setup.py register sdist upload

clean:
	find . -name '*.pyc' -exec rm --force {} +
	rm -rf $(VENV_NAME) *.eggs *.egg-info dist build docs/_build .mypy_cache .cache
