##############################################
# Targets one probably wants

build: build-container
.PHONY: build

build-image:
.PHONY: build-image

build-container:
.PHONY: build-container

run: build
	docker container restart "$(TAG)"
.PHONY: run

shell: build
	docker run -it "$(TAG)" /bin/bash
.PHONY: shell

clean:
.PHONY: clean

clean-docker: clean
.PHONY: clean-docker

##############################################
# Rules to help make interact better with docker

always:
	@true
.PHONY: always

ifndef BUILD_DIR
BUILD_DIR = .
endif

##############################################################
#
# Making images
#
##############################################################
%.image:
	docker build $(BUILD_ARGS_$(*)) -t "$(*)" .
	@touch $(*).image

build-image-%:
	@make --no-print-directory $(patsubst %,timecheck-image-%,$(PREREQ_IMAGES_$(*))) "timecheck-image-$(*)"
	@make --no-print-directory $(patsubst %,%.image,$(PREREQ_IMAGES_$(*))) "$(*).image"

timecheck-image-%:
	@TAG=$$(echo "$(*)" | sed -e 's/@/:/'); \
	DATE=$$(docker image inspect "$${TAG}" --format '{{.Created}}' 2>/dev/null); \
	if [ -n "$${DATE}" ]; then \
		echo "::: $${TAG} image exists with date $${DATE}"; \
		touch "$(*).image" -d "$${DATE}"; \
	else \
		rm -f "$(*).image"; \
	fi

clean-image-%:
	rm -f "$(*).image"

clean-docker-image-%: clean-image-%
	docker image rm -f "$(*)" >/dev/null 2>&1 || true

##############################################################
#
# Making containers
#
##############################################################
%.container: %.image
	@DATE=$$(docker image inspect "$${TAG}" --format '{{.Created}}' 2>/dev/null); \
	if [ -n "$${DATE}" ]; then \
		docker container rm "$*" > /dev/null; \
	fi
	docker container create --name "$(*)" "$(*)"
	@touch "$(*).container"

build-container-%: build-image-%
	@make --no-print-directory "timecheck-container-$(*)"
	@make --no-print-directory "$(*).container"

timecheck-container-%:
	@DATE=$$(docker image inspect "$${TAG}" --format '{{.Created}}' 2>/dev/null); \
	if [ -n "$${DATE}" ]; then \
		echo "::: $${TAG} container exists with date $${DATE}"; \
		touch "$(*).container" -d "$${DATE}"; \
	else \
		rm -f "$(*).container"; \
	fi

clean-container-%:
	rm -f "$(*).container"

clean-docker-container-%:
	docker container rm -f "$(*)" >/dev/null 2>&1 || true
