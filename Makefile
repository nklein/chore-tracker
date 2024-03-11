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
