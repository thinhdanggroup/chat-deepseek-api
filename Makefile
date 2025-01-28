

build-package:
	@rm -rf dist/*
	@python -m venv venv && source venv/bin/activate 
	@python -m build 
	@twine check dist/*

distribute:
	@python -m twine upload dist/*


