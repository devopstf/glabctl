.PHONY: help
.DEFAULT_GOAL := help

resolve-dependencies: ## Install all python dependencies through pip
	@echo "[Dependencies] Resolve all dependencies using 'pip'"
	@pip install --upgrade python-gitlab Click
	@echo "[OK] All dependencies resolved"

install: # Install my script in /usr/bin
	@echo "[Script installation] Create a symbolic link from <here> to </usr/local/bin>"
	@ln -s ${PWD}/main.py /usr/local/bin/gcli
	@echo "[OK] Script installed on </usr/local/bin> correctly. Try 'gcli --help'!"
