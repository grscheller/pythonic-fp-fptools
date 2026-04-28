# Makefile for Sphinx documentation
#
# Important Note: "make devel" and "make release" will just
# use the first pythonic_fp.circulararray package found.

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

STATICDIR     = source/_static
TEMPLATEDIR   = source/_templates

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

setup_devel:
	rm -rf "$(BUILDDIR)"/development
	cp index_devel.rst "$(SOURCEDIR)"/index.rst
	cp conf_devel.py "$(SOURCEDIR)"/conf.py

setup_release:
	rm -rf "$(BUILDDIR)"/release
	cp index_release.rst "$(SOURCEDIR)"/index.rst
	cp conf_release.py "$(SOURCEDIR)"/conf.py

setup_custom:
	rm -rf "$(BUILDDIR)"/custom
	cp index_custom.rst "$(SOURCEDIR)"/index.rst
	cp conf_custom.py "$(SOURCEDIR)"/conf.py

clean_source:
	@rm -f "$(SOURCEDIR)"/conf.py "$(SOURCEDIR)"/index.rst

clean_devel: clean_source
	@rm -rf "$(BUILDDIR)"/development

clean_release: clean_source
	@rm -rf "$(BUILDDIR)"/release

clean_custom: clean_source
	@rm -rf "$(BUILDDIR)"/custom

clean: clean_devel clean_release clean_custom
	@echo Removed all doc build artifacts.

.PHONY: help Makefile
.PHONY: setup_devel setup_release setup_custom
.PHONY: devel release
.PHONY: clean_source clean_devel clean_release clean_custom clean

# Build development labeled html docs.
devel: Makefile setup_devel
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)"/development $(SPHINXOPTS)

# Build release labeled html docs.
release: Makefile setup_release
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)"/release $(SPHINXOPTS)

# Catch-all target: route all unknown targets to Sphinx and save to $(BUILDDIR)/custom.
# Use conf_custom.py and index_custom.html to configure.
%: Makefile setup_custom
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)"/custom $(SPHINXOPTS)
