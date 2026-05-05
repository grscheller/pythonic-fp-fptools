# Makefile for Sphinx documentation

# Last and future releases
#  - former needs to agree with PyPI
#  - later needs to agree with pyproject.toml
PROJECT_NAME = FP Tools Array
PYPI_NAME = fptools
RELEASE_VERSION = 5.2.0
DEVEL_VERSION = 5.2.1
CUSTOM_VERSION = 0.0.0

SPHINXOPTS ?=
SPHINXBUILD ?= sphinx-build
SOURCEDIR = source
BUILDDIR = build

STATICDIR = source/_static
TEMPLATEDIR = source/_templates

# Put help first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

clean_source:
	@rm -f "$(SOURCEDIR)"/conf.py

clean_devel:
	@rm -rf "$(BUILDDIR)"/development

clean_release:
	@rm -rf "$(BUILDDIR)"/release

clean_custom:
	@rm -rf "$(BUILDDIR)"/custom

clean: clean_devel clean_release clean_custom clean_source
	@rm -rf $(BUILDDIR)
	@echo Removed all doc build artifacts.

setup_devel: clean_devel
	@./gen_conf.py devel "$(DEVEL_VERSION)" "$(PROJECT_NAME)" "$(PYPI_NAME)" > "$(SOURCEDIR)"/conf.py

setup_release: clean_release
	@./gen_conf.py release "$(RELEASE_VERSION)" "$(PROJECT_NAME)" "$(PYPI_NAME)" > "$(SOURCEDIR)"/conf.py

setup_custom: clean_custom
	@./gen_conf.py custom "$(CUSTOM_VERSION)" "$(PROJECT_NAME)" "$(PYPI_NAME)" > "$(SOURCEDIR)"/conf.py

setup_redo: clean_custom
	@echo Redoing custom build with a possibly reeditted conf.py
	@./gen_conf.py redo "" "" ""

# Build development labeled html docs.
devel: Makefile setup_devel
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)"/development $(SPHINXOPTS)

# Build release labeled html docs.
release: Makefile setup_release
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)"/release $(SPHINXOPTS)

# Build custom labeled html docs.
custom: Makefile setup_custom
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)"/custom $(SPHINXOPTS)

# Build HTML docs with previous generated (possibly hand edited) source/conf.py,
# put results in $(BUILDDIR)/custom.
redo: Makefile setup_redo
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)"/custom $(SPHINXOPTS)

# Catch-all target: route all unknown targets to Sphinx and save to $(BUILDDIR)/custom.
# Reuse a previously generated source/conf.py.
%: Makefile setup_redo
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)"/custom $(SPHINXOPTS)

.PHONY: help Makefile
.PHONY: setup_devel setup_release setup_custom
.PHONY: devel release
.PHONY: clean_source clean_devel clean_release clean_custom clean
