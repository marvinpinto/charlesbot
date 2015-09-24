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

# Utility target for checking required parameters
guard-%:
	@if [ "$($*)" = '' ]; then \
     echo "Missing required $* variable."; \
     exit 1; \
   fi;

clean:
	py3clean .
	rm -f .coverage
	find . -name "__pycache__" -exec /bin/rm -rf {} \;

clean-all: clean
	rm -rf env
	rm -rf charlesbot.egg-info

env: clean
	test -d $(ENV) || pyvenv-3.4 $(ENV)

install: env
	$(ENV)/bin/pip install -r requirements-dev.txt
	$(ENV)/bin/pip install -e .

checkstyle: install
	$(ENV)/bin/flake8 --max-complexity 10 charlesbot
	$(ENV)/bin/flake8 --max-complexity 10 tests

test: install
	$(ENV)/bin/nosetests \
		-v \
		--with-coverage \
		--cover-package=charlesbot \
		tests

run:
	PYTHONWARNINGS=default PYTHONASYNCIODEBUG=1 $(ENV)/bin/charlesbot

release: guard-PART
	$(ENV)/bin/bumpversion $(PART)
