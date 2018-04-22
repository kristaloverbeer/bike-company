build:
	@docker-compose --project-directory ./ -f docker/docker-compose.yml build --no-cache
run: build
	@docker-compose --project-directory ./ -f docker/docker-compose.yml up -d
sh:
	@docker exec -it gateway /bin/sh
upgrade:
	@docker exec -it gateway flask db upgrade
typing-check:
	@docker exec -it gateway mypy src/ --ignore-missing-imports
syntax-check:
	@docker exec -it gateway flake8
tests:
	@docker exec -it gateway pytest
stop:
	@docker-compose --project-directory ./ -f docker/docker-compose.yml stop
clean: stop
	@docker-compose --project-directory ./ -f docker/docker-compose.yml rm -vf gateway
clean-dangling-images: clean
	@docker rmi -f $(docker images -q --filter "dangling=true")

.PHONY: build run sh upgrade typing-check syntax-check tests stop clean clean-dangling-images
