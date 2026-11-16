# Makefile for Sphinx documentation

# Next four are the source of truth - what is in pyproject.toml
# should agree with first two and one of the last two.
PROJECT_NAME = FPTools
PYPI_NAME = fptools
CURR_RELEASE_VERSION = 6.2.0
DEVEL_VERSION = 6.2.0
PREV_RELEASE_VERSION = 6.1.0

SPHINXOPTS ?=
SPHINXBUILD ?= sphinx-build

# Give build info if "make" without arguments is given
help:
	@echo To build docs: uv run make {devel | curr_release | prev_release}

clean_source:
	@rm -f source/conf.py

clean_prev_release:
	@rm -rf build/prev_release

clean_curr_release:
	@rm -rf build/curr_release

clean_devel:
	@rm -rf devel

clean_index_html:
	@rm -f build/index.html

clean: clean_prev_release clean_curr_release clean_devel clean_source clean_index_html
	@echo Removed all doc build artifacts.

build/index.html: index.html.in Makefile
	@mkdir -p build
	@sed -e 's/@DEVEL@/$(DEVEL_VERSION)/g' \
		 -e 's/@CURR_RELEASE@/$(CURR_RELEASE_VERSION)/g' \
		 -e 's/@DEVEL@/$(DEVEL_VERSION)/g' \
		 -e 's/@PREV_RELEASE@/$(PREV_RELEASE_VERSION)/g' \
		 -e 's/@PROJECTNAME@/$(PROJECT_NAME)/g' \
		 -e 's/@PYPINAME@/$(PYPI_NAME)/g' \
		 $< > $@

devel:        DOCS_TYPE = devel
devel:        VERSION   = $(DEVEL_VERSION)
devel:        OUTDIR    = devel
curr_release: DOCS_TYPE = curr_release
curr_release: VERSION   = $(CURR_RELEASE_VERSION)
curr_release: OUTDIR    = build/curr_release
prev_release: DOCS_TYPE = prev_release
prev_release: VERSION   = $(PREV_RELEASE_VERSION)
prev_release: OUTDIR    = build/prev_release

# The published builds also need the landing page
curr_release prev_release: build/index.html

devel curr_release prev_release:
	@rm -rf '$(OUTDIR)'
	@python3 gen_conf.py $(DOCS_TYPE) '$(VERSION)' '$(PROJECT_NAME)' '$(PYPI_NAME)' > source/conf.py
	@echo Generated source/conf.py for $(DOCS_TYPE)
	@$(SPHINXBUILD) -b html source '$(OUTDIR)' $(SPHINXOPTS)

# Expose Makefile variables to scripts: make print-DEVEL_VERSION
print-%:
	@echo $($*)

.PHONY: help clean clean_source clean_index_html
.PHONY: clean_prev_release clean_curr_release clean_devel
.PHONY: curr_release prev_release devel

# Due to both builds needing to share the generated source/conf.py
.NOTPARALLEL:
