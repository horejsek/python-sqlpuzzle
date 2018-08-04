.PHONY: all
all: sphinx

BUILDDIR=../../python-sqlpuzzle-doc
SPHINXOPTS=-n -W -d $(BUILDDIR)/doctrees .

.PHONY: sphinx
sphinx:
	sphinx-build -b html $(SPHINXOPTS) $(BUILDDIR)/html

.PHONY: clean
clean:
	rm -rf build
