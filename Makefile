run:
	sudo docker build . -t polyhx/python-test
	sudo docker run --rm -it -p 8080:8080 -t polyhx/python-test

build:
	sudo docker build . -t

build-deps:
	sudo docker build . -t polyhx/python-seed
