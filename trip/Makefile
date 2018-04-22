build:
	@docker-compose --project-directory ./ -f docker/docker-compose.yml build --no-cache
run: build
	@docker-compose --project-directory ./ -f docker/docker-compose.yml up -d
sh:
	@docker exec -it trip /bin/sh
upgrade:
	@docker exec -it trip flask db upgrade
typing-check:
	@docker exec -it trip mypy src/ --ignore-missing-imports
syntax-check:
	@docker exec -it trip flake8
tests:
	@docker exec -it trip pytest
stop:
	@docker-compose --project-directory ./ -f docker/docker-compose.yml stop
clean: stop
	@docker-compose --project-directory ./ -f docker/docker-compose.yml rm -vf trip trip_database
clean-dangling-images: clean
	@docker rmi -f $(docker images -q --filter "dangling=true")

.PHONY: build run sh upgrade typing-check syntax-check tests stop clean clean-dangling-images
