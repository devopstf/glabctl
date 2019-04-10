.PHONY: help
.DEFAULT_GOAL := help

resolve-dependencies: ## Install all python dependencies through pip
	@echo "[Dependencies] Resolve all dependencies using 'pip3'"
	@pip3 install --upgrade python-gitlab gitlab Click click_help_colors
	@echo "[OK] All dependencies resolved"

install: # Install my script in /usr/bin
	@echo "[Script installation] Create a symbolic link from <here> to </usr/local/bin>"
	@ln -fs ${PWD}/main.py /usr/local/bin/glabctl
	@echo "[OK] Script installed on </usr/local/bin> correctly. Try 'glabctl --help'!"

install-docker: # Install PGCLI using Docker
	@echo "[Docker] Building the image from 0."
	@docker build -t pgcli:latest -f ./docker/Dockerfile .
	@echo "[Script installation] Creating symbolic link from <docker/bin/pgcli> to </usr/local/bin>"
	@ln -fs ${PWD}/docker/bin/pgcli /usr/local/bin/pgcli
	@echo "[OK] Script installed on </usr/local/bin> correctly. Try 'pgcli --help'!"
