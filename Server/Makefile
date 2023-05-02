DOCKER_IMAGE:=server
help:
	@echo "make <target>"
	@echo "  help       Show this help"
	@echo "  build      Build the server docker image"
	@echo "  run 		Run the built image"
build:
	docker build --tag ${DOCKER_IMAGE} .

run:
	docker run --rm -it --publish 80:8000 ${DOCKER_IMAGE}
