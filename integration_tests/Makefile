.PHONY: test-setup tests

test-setup:
	docker pull python:2.7
	docker pull n3llyb0y/wait
	docker pull progrium/consul
	docker build -t xivo/xivo-backup ..
	docker build -t xivo-backup-tests -f Dockerfile ..
	docker build -t xivo-backup-tests-data -f Dockerfile-data ..

test:
	nosetests
