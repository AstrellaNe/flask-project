start:
	flask --app example --debug run --port 8000

install:
	poetry install

build:
	poetry build

publish: 
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl
	
package-reinstall:
	pip install --user --force-reinstall dist/*.whl


lint:	
	poetry run flake8

git-prepare:
	make build
	make package-reinstall
	git add