#!/usr/bin/env python

"""The setup script."""


from setuptools import find_packages, setup

from zemfrog import __author__, __email__, __version__

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

with open("requirements.txt") as req:
    requirements = req.read().splitlines()

with open("requirements-dev.txt") as req:
    test_requirements = req.read().splitlines()

setup_requirements = []


project_urls = {
    "Github": "https://github.com/zemfrog/zemfrog",
    "Issue Tracker": "https://github.com/zemfrog/zemfrog/issues",
    "Donation": "https://www.patreon.com/aprilahijriyan",
}

setup(
    author=__author__,
    author_email=__email__,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Flask",
        # "Framework :: Zemfrog",
        # "Framework :: Zemfrog :: " + __version__,
    ],
    description="Zemfrog is a simple framework based on flask for building a REST API quickly.",
    entry_points={"console_scripts": ["zemfrog=zemfrog.cli:main"]},
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="flask wsgi web zemfrog api",
    name="zemfrog",
    packages=find_packages(include=["zemfrog", "zemfrog.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/zemfrog/zemfrog",
    version=__version__,
    zip_safe=False,
    project_urls=project_urls,
)
