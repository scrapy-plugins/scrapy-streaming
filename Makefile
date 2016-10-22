NODE_DIR = helpers/nodejs

test:
	tox
	$(MAKE) -C $(NODE_DIR) test

lint:
	$(MAKE) -C $(NODE_DIR) lint

.PHONY: test lint
