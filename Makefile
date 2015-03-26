.PHONY: all requirements test-requirements test clean pyflakes unittest unittest-coverage fulltest install reinstall

PYTHON_FIND=find picas tests -name '*.py'

all: install

requirements:
	@pip install -r requirements.txt

install: requirements
	@pip install .
	
reinstall:
	@pip install --upgrade --no-deps .

pyflakes:
	@echo "=======  PyFlakes  ========="
	@$(PYTHON_FIND) -exec pyflakes {} \;

pep8:
	@echo "=======   PEP8     ========="
	@$(PYTHON_FIND) -exec pep8 {} \;

unittest:
	@echo "======= Unit Tests ========="
	@nosetests

test-requirements: requirements
	@pip install -r test_requirements.txt

test: test-requirements pyflakes unittest

unittest-coverage:
	@echo "======= Unit Tests ========="
	@nosetests --with-coverage

fulltest: test-requirements pep8 pyflakes unittest-coverage

clean: 
	rm -rf build/
	find . -name *.pyc -delete
	find . -name *.pyo -delete

