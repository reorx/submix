.PHONY: test build requirements.lock

clean:
	rm -rf build dist *.egg-info

test:
	PYTHONPATH=. pytest -v test/

requirements.lock:
	pip-compile --output-file=requirements.lock

build:
	python setup.py build

build-dist:
	python setup.py sdist bdist_wheel

publish: build-dist
	python -m twine upload --skip-existing $(shell ls -t dist/*.whl | head -1)
