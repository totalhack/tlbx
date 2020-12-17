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

# Split git requirements to fill in dependency_links
git_requires = [x for x in requires if "git" in x]
non_git_requires = [x for x in requires if "git" not in x]
for repo in git_requires:
    # Append git egg references
    non_git_requires.append(repo.split("egg=")[-1])

extras_require = {
    "pandas": ["pandas~=1.1.5"],
    "dev": ["black", "pre-commit", "pylint", "pytest~=5.3.2", "twine~=3.1.1", "wheel"],
}
extras_require["complete"] = sorted(set(sum(extras_require.values(), [])))

exec(open("tlbx/version.py").read())

setup(
    name="tlbx",
    description="Just some common utilities.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/totalhack/tlbx",
    author="totalhack",
    author_email="none@none.com",
    maintainer="totalhack",
    version=__version__,
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
    packages=find_packages(exclude=["tests.*", "tests"]),
    include_package_data=True,
    install_requires=non_git_requires,
    dependency_links=git_requires,
    extras_require=extras_require,
)
