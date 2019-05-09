EMPRESS_PY = empress.py
EMPRESS = empress

INSTALL = install
PREFIX = /usr/local/bin

.NOTPARALLEL:

.PHONY: all
all:

.PHONY: install
install:
	$(INSTALL) -Dm 0755 $(EMPRESS_PY) $(DESTDIR)$(PREFIX)/$(EMPRESS)

.PHONY: uninstall
uninstall:
	$(RM) $(DESTDIR)$(PREFIX)/$(EMPRESS)

.PHONY: clean
clean:

