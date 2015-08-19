.PHONY: test-setup tests

test-setup:
	docker pull python:2.7
	docker pull n3llyb0y/wait
	docker pull progrium/consul
	docker build -t xivo/xivo-backup ..
	docker build --no-cache -t xivo-backup-test -f Dockerfile ..

test:
	nosetests
