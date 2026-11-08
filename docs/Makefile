# Makefile for Sphinx documentation

# Next four are the source of truth - what is in pyproject.toml
# should agree with first two and one of the last two.
PROJECT_NAME = FPTools
PYPI_NAME = fptools
CURR_ROLLING_RELEASE_VERSION = 6.2.0
DEVEL_VERSION = 6.2.1
PREV_ROLLING_RELEASE_VERSION = 6.1.0

SPHINXOPTS ?=
SPHINXBUILD ?= sphinx-build
SOURCEDIR = source
BUILDDIR = build

# Give build info if "make" without arguments is given
help:
	@echo To build docs: uv run make {devel | curr_release | prev_release}

clean_source:
	@rm -f "$(SOURCEDIR)"/conf.py

clean_prev_release:
	@rm -rf "$(BUILDDIR)"/prev_release

clean_curr_release:
	@rm -rf "$(BUILDDIR)"/curr_release

clean_devel:
	@rm -rf "$(BUILDDIR)"/devel

clean_index_html:
	@rm -f "$(BUILDDIR)"/index.html

clean: clean_prev_release clean_curr_release clean_devel clean_source clean_index_html
	@echo Removed all doc build artifacts.

setup_curr_release: clean_curr_release clean_index_html
	@python3 gen_conf.py curr_release "$(CURR_ROLLING_RELEASE_VERSION)" "$(PROJECT_NAME)" "$(PYPI_NAME)" > "$(SOURCEDIR)"/conf.py
	@echo Generating source/conf.py for current rolling release

setup_prev_release: clean_prev_release clean_index_html
	@python3 gen_conf.py prev_release "$(PREV_ROLLING_RELEASE_VERSION)" "$(PROJECT_NAME)" "$(PYPI_NAME)" > "$(SOURCEDIR)"/conf.py
	@sed -e 's/@CURR_RELEASE@/$(CURR_ROLLING_RELEASE_VERSION)/g'
	@echo Generating source/conf.py for previous rolling release

setup_devel: clean_devel clean_index_html
	@python3 gen_conf.py devel "$(DEVEL_VERSION)" "$(PROJECT_NAME)" "$(PYPI_NAME)" > "$(SOURCEDIR)"/conf.py
	@echo Generating source/conf.py for devel

$(BUILDDIR)/index.html: index.html.in Makefile
	@mkdir -p $(BUILDDIR)
	@sed -e 's/@CURR_RELEASE@/$(CURR_ROLLING_RELEASE_VERSION)/g' \
	     -e 's/@DEVEL@/$(DEVEL_VERSION)/g' \
         -e 's/@PREV_RELEASE@/$(PREV_ROLLING_RELEASE_VERSION)/g' \
	     -e 's/@PROJECTNAME@/$(PROJECT_NAME)/g' \
	     -e 's/@PYPINAME@/$(PYPI_NAME)/g' \
	     $< > $@

# Build current rolling release labeled docs
curr_release: setup_curr_release $(BUILDDIR)/index.html
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)"/curr_release $(SPHINXOPTS)

# Build previous rolling release labeled docs
prev_release: setup_prev_release $(BUILDDIR)/index.html
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)"/prev_release $(SPHINXOPTS)

# Build development labeled docs
devel: setup_devel $(BUILDDIR)/index.html
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)"/devel $(SPHINXOPTS)

# Expose Makefile variables to scripts: make print-DEVEL_VERSION
print-%:
	@echo $($*)

.PHONY: help clean clean_source clean_index_html
.PHONY: clean_prev_release clean_curr_release clean_devel
.PHONY: setup_prev_release setup_curr_release setup_devel
.PHONY: curr_release prev_release devel

# Due to both builds needing to share the generated source/conf.py
.NOTPARALLEL:
