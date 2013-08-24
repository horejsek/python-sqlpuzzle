
PYTHON=`which python`
PYTHON3=`which python3`
DESTDIR=/
BUILDIR=$(CURDIR)/debian/sqlpuzzle
PROJECT=sqlpuzzle

all:
	@echo "make source - Create source package"
	@echo "make install - Install on local system"
	@echo "make buildrpm - Generate a rpm package"
	@echo "make builddeb - Generate a deb package"
	@echo "make clean - Get rid of scratch and byte files"

source:
	$(PYTHON) setup.py sdist

upload:
	$(PYTHON) setup.py register sdist upload

install:
	$(PYTHON) setup.py install --root $(DESTDIR)
	$(PYTHON3) setup.py install --root $(DESTDIR)

install-building-packages:
	apt-get install build-essential dh-make debhelper devscripts cdbs
	curl http://python-distribute.org/distribute_setup.py | $(PYTHON3)
	curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | $(PYTHON3)
	curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | $(PYTHON)
	pip install nose
	pip-3.2 install nose

test: test2 test3

test2:
	$(PYTHON) tests/alltests.py

test3:
	$(PYTHON3) tests/alltests.py

buildrpm:
	$(PYTHON) setup.py bdist_rpm --post-install=rpm/postinstall --pre-uninstall=rpm/preuninstall

builddeb:
	# build the source package in the parent directory
	# then rename it to project_version.orig.tar.gz
	$(PYTHON) setup.py sdist --dist-dir=../ --prune
	rename -f 's/$(PROJECT)-(.*)\.tar\.gz/$(PROJECT)_$$1\.orig\.tar\.gz/' ../*
	# build the package
	dpkg-buildpackage -i -I -rfakeroot

localdev:
	cp git-hooks/* .git/hooks/
	chmod 755 .git/hooks/

clean:
	$(PYTHON) setup.py clean
	$(MAKE) -f $(CURDIR)/debian/rules clean
	rm -rf build/ MANIFEST
	find . -name '*.pyc' -delete
