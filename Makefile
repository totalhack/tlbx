PACKAGE := tlbx
ENV := $(VIRTUAL_ENV)
TEST_ENV := /tmp/tlbx_pip_test
PIP := $(ENV)/bin/pip
SETUP := $(ENV)/bin/python setup.py
VERSION := $(shell python setup.py --version)

clean:
	rm -rf build dist *.egg-info

develop:
	$(PIP) install -U -e ./ --no-binary ":all:"

install:
	$(SETUP) bdist_wheel egg_info
	$(PIP) install dist/$(PACKAGE)-$(VERSION)-py3-none-any.whl

uninstall:
	if ($(PIP) freeze 2>&1 | grep $(PACKAGE)); \
		then $(PIP) uninstall $(PACKAGE) --yes; \
	else \
		echo 'Package not installed'; \
	fi

dist:
	$(MAKE) clean
	$(SETUP) sdist bdist_wheel

upload:
	$(ENV)/bin/python -m twine upload --repository pypi dist/*

test_upload:
	$(ENV)/bin/python -m twine upload --repository testpypi dist/*

test_venv:
	rm -rf $(TEST_ENV)
	mkdir $(TEST_ENV)
	$(ENV)/bin/python -m venv $(TEST_ENV)
	$(TEST_ENV)/bin/pip install -U pip

pip:
	$(MAKE) dist
	$(MAKE) upload
	$(MAKE) test_venv
	sleep 30
	$(TEST_ENV)/bin/pip install -U tlbx==$(VERSION)
	$(TEST_ENV)/bin/python -c "import tlbx"

test_pip:
	$(MAKE) dist
	$(MAKE) test_upload
	$(MAKE) test_venv
	sleep 30
	$(TEST_ENV)/bin/pip install -i "https://test.pypi.org/simple/" --extra-index-url "https://pypi.org/simple/" tlbx==$(VERSION)
	$(TEST_ENV)/bin/python -c "import tlbx"

.PHONY: dist clean test_venv
