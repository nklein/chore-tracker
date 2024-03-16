################################################################################################
INSTALL_DIR := /usr/local/chore-tracker

################################################################################################
VENV := $(INSTALL_DIR)/python-venv
IN_VENV := . $(VENV)/bin/activate &&

################################################################################################
install: install-packages install-app install-config install-bin
.PHONY: install

install-packages: $(INSTALL_DIR)/requirements.txt
.PHONY: install-packages

install-app: $(INSTALL_DIR)
	rsync -a --exclude=__pycache__ --exclude=config.json app $(INSTALL_DIR)
.PHONY: install-app

install-config: $(INSTALL_DIR)/app/config.json
.PHONY: install-config

install-bin: $(INSTALL_DIR)
	rsync -a --exclude=__pycache__ --exclude=config.json bin $(INSTALL_DIR)
.PHONY: install-bin

################################################################################################
$(VENV):
	@[ -d $(INSTALL_DIR) ] || make $(INSTALL_DIR)
	python3 -m venv $(VENV)

$(INSTALL_DIR):
	sudo mkdir -p $(@)
	sudo chown $(USER) $(@)

$(INSTALL_DIR)/requirements.txt: $(VENV) requirements.txt
	$(IN_VENV) pip3 install --no-cache-dir -r requirements.txt
	cp requirements.txt $(@D)

$(INSTALL_DIR)/app/config.json:
	cp -p app/config.json $(@)
