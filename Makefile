build: clean
	bash ./bin/build.sh

clean:
	-rm -r crucyble* dist build

upload:
	twine upload --repository-url https://test.pypi.org/legacy/ *.tar.gz