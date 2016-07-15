requirements:
	npm install

test: requirements
	./node_modules/.bin/mocha --reporter spec

lint: requirements
	./node_modules/eslint/bin/eslint.js index.js

check: test lint

.PHONY:	requirements test lint check
