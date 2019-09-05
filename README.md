toolbox: just some common utilities
===================================

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Installation
------------

To install from source and setup development in your virtual environment:

```shell
git clone https://github.com/totalhack/toolbox.git
cd toolbox
pip install -r requirements.txt
pre-commit install 
make ENV=/path/to/venv develop # or 'make ENV=/path/to/venv install'
```

To add as a dependency for your existing project:

```shell
cd yourproject
echo "git+git://github.com/totalhack/toolbox.git#egg=toolbox" >> requirements.txt
pip install -r requirements.txt
```
