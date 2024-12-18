# See: https://earthly.dev/blog/python-makefile/
# See: https://medium.com/aigent/makefiles-for-python-and-beyond-5cf28349bf05

PYTHON := python3.12
VENV := .venv
REQUIREMENTS := requirements.txt

.PHONY: all venv install clean

all: venv install

venv:
	@echo $(ROOT_DIR)
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV)

install: venv
	@echo "Installing dependencies..."
	@$(VENV)/bin/pip install -r $(REQUIREMENTS)
# Based on https://stackoverflow.com/questions/4757178/how-do-you-set-your-pythonpath-in-an-already-created-virtualenv/47184788#47184788
	@echo ${CURDIR}/../ > $(VENV)/lib/$(PYTHON)/site-packages/bazaarlibs.pth

clean:
	@echo "Cleaning up..."
	@rm -rf	$(VENV)
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete

help:
	@echo "Available targets:"
	@echo "  all       : Set up virtual environment and install dependencies (default)"
	@echo "  venv      : Create virtual environment"
	@echo "  install   : Install dependencies from requirements.txt"
	@echo "  clean     : Remove virtual environment and Python cache files"
	@echo "  help      : Show this help message"