# Makefile for Sphinx documentation
#
#   uv run make devel          build docs for the working tree  -> devel/
#   make curr_release          build docs for the installed pkg -> build/curr_release/
#   make prev_release          build docs for the installed pkg -> build/prev_release/
#
# Only build/ is deployed to GitHub Pages. The two release targets document
# whatever version of the package is installed in the active environment;
# the versions below tell CI which ones to install from PyPI and are shown
# on the landing page.

PROJECT_NAME = Gadgets
PYPI_NAME = gadgets
CURR_RELEASE_VERSION = 6.0.0
PREV_RELEASE_VERSION = 4.6.0

SPHINXOPTS ?=
SPHINXBUILD ?= sphinx-build

# source/conf.py reads these from the environment
export PROJECT_NAME PYPI_NAME DOCS_TYPE

help:
	@echo 'To build docs: uv run make {devel | curr_release | prev_release}'

devel:        DOCS_TYPE = devel
devel:        OUTDIR    = devel
curr_release: DOCS_TYPE = curr_release
curr_release: OUTDIR    = build/curr_release
prev_release: DOCS_TYPE = prev_release
prev_release: OUTDIR    = build/prev_release

# The published builds also need the landing page
curr_release prev_release: build/index.html

devel curr_release prev_release:
	@rm -rf '$(OUTDIR)'
	@$(SPHINXBUILD) -b html source '$(OUTDIR)' $(SPHINXOPTS)

build/index.html: index.html.in Makefile
	@mkdir -p build
	@sed -e 's/@CURR_RELEASE@/$(CURR_RELEASE_VERSION)/g' \
	     -e 's/@PREV_RELEASE@/$(PREV_RELEASE_VERSION)/g' \
	     -e 's/@PROJECTNAME@/$(PROJECT_NAME)/g' \
	     -e 's/@PYPINAME@/$(PYPI_NAME)/g' \
	     $< > $@

clean:
	@rm -rf build devel
	@echo Removed all doc build artifacts.

# Expose Makefile variables to scripts: make print-CURR_RELEASE_VERSION
print-%:
	@echo $($*)

.PHONY: help clean devel curr_release prev_release
