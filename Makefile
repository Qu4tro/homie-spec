.PHONY: all test tests cov-report tests-all style black lint types docs tox mypy pdoc pylint clean test-watch tests-watch watch ptw travis travis-lint pdocs type


test tests .coverage:
	tox -e py38

test-watch tests-watch watch ptw:
	poetry run ptw -- --mypy

cov-report: .coverage
	poetry run coverage report -m

tests-all tox:
	tox

style black:
	poetry run black .

lint pylint:
	poetry run pylint */*.py

travis travis-lint:
	cat .travis.yml | docker run tianon/travis-cli lint -

type types mypy:
	poetry run mypy .

docs pdoc pdocs:
	poetry run pdoc --force --config show_type_annotations=True --html --output-dir docs $$(poetry version | cut -f1 -d' ' | sed 's/-/_/g')
	mv docs/$$(poetry version | cut -f1 -d' ' | sed 's/-/_/g')/* docs
	rmdir docs/$$(poetry version | cut -f1 -d' ' | sed 's/-/_/g')

clean:
	rm -rf __pycache__ */__pycache__ *.egg-info .coverage .hypothesis .mypy_cache .tox .pytest_cache
