# Makefile for Sphinx documentation

# Next four are the source of truth - what is in pyproject.toml
# should agree with first two and one of the last two.
PROJECT_NAME = FP Tools Array
PYPI_NAME = fptools
RELEASE_VERSION = 6.1.0
DEVEL_VERSION = 6.2.0

SPHINXOPTS ?=
SPHINXBUILD ?= sphinx-build
SOURCEDIR = source
BUILDDIR = build

# Put help first so that "make" without argument is like "make help"
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

clean_source:
	@rm -f "$(SOURCEDIR)"/conf.py

clean_devel:
	@rm -rf "$(BUILDDIR)"/development

clean_release:
	@rm -rf "$(BUILDDIR)"/release

clean_index_html:
	@rm -f "$(BUILDDIR)"/index.html

clean: clean_devel clean_release clean_source clean_index_html
	@echo Removed all doc build artifacts.

setup_devel: clean_devel clean_index_html
	@./gen_conf.py devel "$(DEVEL_VERSION)" "$(PROJECT_NAME)" "$(PYPI_NAME)" > "$(SOURCEDIR)"/conf.py
	@echo Generating source/conf.py for devel

setup_release: clean_release clean_index_html
	@./gen_conf.py release "$(RELEASE_VERSION)" "$(PROJECT_NAME)" "$(PYPI_NAME)" > "$(SOURCEDIR)"/conf.py
	@echo Generating source/conf.py for release

$(BUILDDIR)/index.html: index.html.in Makefile
	@sed -e 's/@RELEASE@/$(RELEASE_VERSION)/g' \
	     -e 's/@DEVEL@/$(DEVEL_VERSION)/g' \
	     -e 's/@PROJECTNAME@/$(PROJECT_NAME)/g' \
	     -e 's/@PYPINAME@/$(PYPI_NAME)/g' \
	     $< > $@

# Build development labeled docs
devel: setup_devel $(BUILDDIR)/index.html
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)"/development $(SPHINXOPTS)

# Build release labeled docs
release: setup_release $(BUILDDIR)/index.html
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)"/release $(SPHINXOPTS)

# Expose Makefile variables to scripts: make print-RELEASE_VERSION
print-%:
	@echo $($*)

.PHONY: help setup_devel setup_release devel release
.PHONY: clean_source clean_devel clean_release clean_index_html clean

# Due to both builds needing to share the generated source/conf.py
.NOTPARALLEL:
