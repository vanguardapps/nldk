#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="nldk",
    version="0.1.0-alpha.1",
    description="Tools for handling baseline tasks related to natural language processing.",
    long_description="Tools for handling baseline tasks related to natural language processing.",
    url="https://github.com/vanguardapps/nldk",
    download_url="https://pypi.python.org/pypi/nldk",
    license="MIT",
    author="Roy McClanahan",
    author_email="rmcclanahan@vanguardapps.io",
    maintainer="Roy McClanahan",
    maintainer_email="rmcclanahan@vanguardapps.io",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Utilities",
        "Topic :: Text Processing :: General",
    ],
    packages=find_packages(),
    install_requires=[
        "regex==2023.10.3",
        "nltk==3.8.1",
    ],
    scripts=["nldk/bin/nldk"],
)
