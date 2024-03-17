################################################################################################
INSTALL_DIR := /usr/local/chore-tracker

################################################################################################
VENV := $(INSTALL_DIR)/python-venv
IN_VENV := . $(VENV)/bin/activate &&

################################################################################################
install: install-packages install-app install-config install-bin install-lib
.PHONY: install

install-packages: $(INSTALL_DIR)/requirements.txt
.PHONY: install-packages

install-app: $(INSTALL_DIR)
	rsync -a --exclude=__pycache__ app $(INSTALL_DIR)
.PHONY: install-app

install-config: $(INSTALL_DIR)/etc/config.json
.PHONY: install-config

install-bin: $(INSTALL_DIR)
	rsync -a bin $(INSTALL_DIR)
.PHONY: install-bin

install-lib: $(INSTALL_DIR)/lib/systemd/chore-tracker.service
.PHONY: install-lib

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

$(INSTALL_DIR)/etc/config.json:
	cp -p etc/config.json $(@)

$(INSTALL_DIR)/lib/systemd/chore-tracker.service: lib/systemd/chore-tracker.service
	@[ -d $(INSTALL_DIR) ] || make $(INSTALL_DIR)
	cp $(<) $(@)
	@if grep -q '##INSTALL_DIR##' $(@); then \
	    sed -i -e "s!##INSTALL_DIR##!$(INSTALL_DIR)!g" $(@) \
	        && sudo systemctl enable $(@) ; \
	fi
