#!/usr/bin/env python

from setuptools import setup

setup(
    name = 'beets-aura',
    version = '0.0.1',
    author = 'Gabriel Schubiner',
    author_email = 'g@gabeos.cc',
    description = ("AURA REST API implementation for Beets music library in Flask"),
    license = "MIT",
    keywords = "audio music api beets aura stream",
    packages = ["aura","test"],
    test_suite = "test"
)
