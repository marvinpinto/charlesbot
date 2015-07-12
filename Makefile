ENV=./env

all: help

help:
	@echo '-------------------------'
	@echo ' charlesbot make targets'
	@echo '-------------------------'
	@echo 'help: This help'
	@echo 'install: Install dev dependencies'
	@echo 'test: Run tests'
	@echo 'checkstyle: Run flake8'
	@echo 'run: Run CharlesBOT locally'

clean:
	py3clean .

clean-all: clean
	rm -rf env
	rm -rf charlesbot.egg-info

env: clean
	test -d $(ENV) || pyvenv-3.4 --without-pip $(ENV)
	test -f $(ENV)/bin/pip || curl https://bootstrap.pypa.io/get-pip.py | $(ENV)/bin/python

install: env
	$(ENV)/bin/pip install -r requirements-dev.txt
	$(ENV)/bin/pip install -e .

freeze: clean-all env
	$(ENV)/bin/pip install -e .
	$(ENV)/bin/pip freeze | sed '/^-e.*/d' > requirements.txt

checkstyle: install
	$(ENV)/bin/flake8 --max-complexity 10 charlesbot
	$(ENV)/bin/flake8 --max-complexity 10 tests

test: install
	$(ENV)/bin/nosetests tests

run:
	$(ENV)/bin/charlesbot
