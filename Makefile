.PHONY: build install

build:
	python -m build

install:
	pip uninstall -y arslabrobotics
	pip install dist/arslabrobotics-2.0.0-py3-none-any.whl
