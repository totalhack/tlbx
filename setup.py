#!/usr/bin/env python

from contextlib import contextmanager
import os

from setuptools import find_packages, setup


@contextmanager
def load_file(fname):
    f = open(os.path.join(os.path.dirname(__file__), fname))
    try:
        yield f
    finally:
        f.close()


with load_file("README.md") as f:
    README = f.read()

with load_file("requirements.txt") as f:
    requires = f.read().split("\n")


exec(open("tlbx/version.py").read())

setup(
    name="tlbx",
    description="Just some common utilities.",
    long_description=README,
    author="totalhack",
    maintainer="totalhack",
    version=__version__,
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
