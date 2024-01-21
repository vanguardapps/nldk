#!/usr/bin/env python


from setuptools import setup


setup(
    name="nldk",
    version="0.1.0",
    description="Tools for handling baseline tasks related to natural language processing.",
    long_description="",
    url="https://github.com/vanguardapps/nldk",
    download_url="https://pypi.python.org/pypi/nldk",
    license="MIT",
    author="Roy McClanahan",
    author_email="rmcclanahan@vanguardapps.io",
    maintainer="Roy McClanahan",
    maintainer_email="rmcclanahan@vanguardapps.io",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    install_requires=[
        "utm",
        "SQLAlchemy>=0.6",
        "BrokenPackage>=0.7,<1.0",
    ],
    dependency_links=[
        "git+https://github.com/Turbo87/utm.git@v0.3.1#egg=utm-0.3.1",
    ],
)
