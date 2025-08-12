publish:
	python3 -m build --wheel
	twine upload dist/* --verbose
test_publish:
# 	python3 -m build --wheel
	twine upload -r testpypi dist/* --verbose -u __token__
