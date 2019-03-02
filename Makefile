build: clean
	bash ./bin/build.sh

clean:
	-rm -r crucyble* dist build

upload:
	twine upload *.tar.gz