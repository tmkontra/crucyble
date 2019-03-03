TAG=$$(grep 'version =' pyproject.toml | cut -d\" -f2)

build: clean
	bash ./bin/build.sh

clean:
	-rm -r crucyble* dist build

upload:
	twine upload *.tar.gz

release: build
	echo "tagging: ${TAG}"
	git tag v${TAG}
	git push origin : v${TAG}
