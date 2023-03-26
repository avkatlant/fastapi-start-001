up_dev:
	docker-compose -f docker-compose-dev.yml up -d

log_dev:
	docker-compose -f docker-compose-dev.yml logs -f

down_dev:
	docker-compose -f docker-compose-dev.yml down && network prune -f

########################### Begin TESTS ###############################

up_test:
	docker-compose -f docker-compose-test.yml up -d --remove-orphans

run_test:
	docker exec -it fastapi_test /bin/bash -c "sleep 3s && pytest"

log_test:
	docker-compose -f docker-compose-test.yml logs -f

down_test:
	docker-compose -f docker-compose-test.yml down

tests:
	make up_test -i
	make run_test -i
	make down_test -i
	make clean

############################## End TESTS ##############################

clean:
	docker container prune -f

.PHONY: tests
