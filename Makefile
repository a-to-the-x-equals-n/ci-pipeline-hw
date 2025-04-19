SHELL := /bin/bash
SHELLFLAGS := -eu -o pipefail -c

.SILENT:
.ONESHELL:
.PHONY: tree \
        jenkins jenkins-start jenkins-stop jenkins-restart jenkins-status jenkins-browser

PY = python
PROJECT = $(shell grep -m 1 '^name =' pyproject.toml | cut -d '"' -f 2)
DEPTH = 4

BU = 94
YW = 93
GR = 92
MG = 35
PR = 38;5;129

I = $(shell printf '\033[1;$(MG)m')   # magenta
O = $(shell printf '\033[1;$(PR)m')   # purple
R = $(shell printf '\033[0m')         # reset

# --- BANNERS ---

define banner-i
	@PHRASE="$(1)"; \
	WIDTH=$$(tput cols); \
	PHRASE_LEN=$${#PHRASE}; \
	PAD=$$(( (WIDTH - PHRASE_LEN - 2) / 2 )); \
	LEFT=$$(printf "%*s" "$$PAD" ""); \
	RIGHT=$$(printf "%*s" "$$PAD" ""); \
	LINE="$${LEFT// /=} $$PHRASE $${RIGHT// /=}"; \
	LINE=$${LINE:3:$$(( $${#LINE} - 4 ))}; \
	echo "$(I)$${LINE}$(R)"
endef

define banner-o
	@PHRASE="$(1)"; \
	WIDTH=$$(tput cols); \
	PHRASE_LEN=$${#PHRASE}; \
	PAD=$$(( (WIDTH - PHRASE_LEN - 2) / 2 )); \
	LEFT=$$(printf "%*s" "$$PAD" ""); \
	RIGHT=$$(printf "%*s" "$$PAD" ""); \
	LINE="$${LEFT// /=} $$PHRASE $${RIGHT// /=}"; \
	LINE=$${LINE:3:$$(( $${#LINE} - 4 ))}; \
	echo "$(O)$${LINE}$(R)"
endef

test-banner:
	$(call banner-i,TEST LINE)

tree:
	$(call banner-i,BUILDING TREEHOUSE)
	@tree -C -L $(DEPTH) -I '__pycache__|*.py[co]|*.sw?|.DS_Store|.git|node_modules|hidden|build|dist|*.egg-info'
	$(call banner-o,TREE BUILT)



# --- JENKINS ---

jenkins-browser:
	$(call banner-i,NAVIGATING TO DASHBOARD)
	@powershell.exe start http://localhost:8080/
	$(call banner-o,DASHBOARD CLOSED)

jenkins-start:
	$(call banner-i,STARTING JENKINS SERVER)
	@sudo service jenkins start
	$(call banner-o,JENKINS STARTED)

jenkins: jenkins-start jenkins-browser

jenkins-stop:
	$(call banner-i,SHUTTING DOWN JENKINS)
	@sudo service jenkins stop
	$(call banner-o,JENKINS OFFLINE)

jenkins-restart:
	$(call banner-i,RESTARTING JENKINS)
	@sudo service jenkins restart
	$(call banner-o,JENKINS RESTARTED)

jenkins-status:
	$(call banner-i,JENKINS STATUS)
	@sudo service jenkins status
	$(call banner-o,STATUS CHECK COMPLETE)


.PHONY: docker docker-build docker-run docker-clean

docker: docker-build docker-run

docker-build:
	$(call banner-i,BUILDING DOCKER IMAGE)
	@docker build -t airline-app .
	$(call banner-o,BUILD COMPLETE)

docker-run:
	$(call banner-i,RUNNING CONTAINER)
	@docker run --rm airline-app
	$(call banner-o,CONTAINER EXITED)

docker-clean:
	$(call banner-i,REMOVING DOCKER IMAGE)
	@docker rmi -f airline-app || true
	$(call banner-o,IMAGE REMOVED)