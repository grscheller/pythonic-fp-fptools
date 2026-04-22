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

Makefile:
	mkdir -p $(STATICDIR) $(TEMPLATEDIR)

# Build development labeled html docs.
devel: Makefile
	rm -rf "$(BUILDDIR)"/development
	rm -f "$(SOURCEDIR)"/index.rst "$(SOURCEDIR)"/conf.py
	cp index_devel.rst "$(SOURCEDIR)"/index.rst
	cp conf_devel.py "$(SOURCEDIR)"/conf.py
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)"/development $(SPHINXOPTS)

# Build release labeled html docs.
release: Makefile
	rm -rf "$(BUILDDIR)"/release
	rm -f "$(SOURCEDIR)"/index.rst "$(SOURCEDIR)"/conf.py
	cp index_release.rst "$(SOURCEDIR)"/index.rst
	cp conf_release.py "$(SOURCEDIR)"/conf.py
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)"/release $(SPHINXOPTS)

.PHONY: help Makefile devel release

# Catch-all target: route all unknown targets to Sphinx, build development docs
%: Makefile
	rm -rf "$(BUILDDIR)"/development
	rm -f "$(SOURCEDIR)"/index.rst "$(SOURCEDIR)"/conf.py
	cp index_devel.rst "$(SOURCEDIR)"/index.rst
	cp conf_devel.py "$(SOURCEDIR)"/conf.py
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)"/development $(SPHINXOPTS)
