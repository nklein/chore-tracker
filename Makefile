TAG := docker-chore-tracker

include docker-support.mk

build-container: build-container-$(TAG)

build-image-$(TAG): Dockerfile requirements.txt
build-image-$(TAG): $(shell find app -type f -print)

clean: clean-image-$(TAG)
clean: clean-docker-image-$(TAG)
clean: clean-container-$(TAG)
clean: clean-docker-container-$(TAG)

clean-docker-image-$(TAG): clean-docker-container-$(TAG)

make-virtual-env: cannot-have-virtual-env
	python3 -m venv $(PWD)/python-venv
.PHONY: make-virtual-env

prepare-virtual-env: need-virtual-env requirements.txt
	pip3 install --no-cache-dir -r requirements.txt
.PHONY: prepare-virtual-env

need-virtual-env:
	@[ -n "${VIRTUAL_ENV}" ]
.PHONY: need-virtual-env

cannot-have-virtual-env:
	@[ -z "${VIRTUAL_ENV}" ]
.PHONY: cannot-have-virtual-env
