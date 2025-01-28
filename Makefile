

distribute:
	@python -m venv venv && source venv/bin/activate && pip install --upgrade pip build twine && python -m build && python -m twine upload dist/*


