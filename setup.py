#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'rueckenwind',
    'docker',
    'pyyaml',
]

test_requirements = [
    'pytest',
    'pytest-tornado',
]

setup(
    name='devenv',
    version='0.1.1',
    description="A development environment based upon docker.",
    long_description=readme + '\n\n' + history,
    author="Florian Ludwig",
    author_email='f.ludwig@greyrook.com',
    url='https://github.com/FlorianLudwig/devenv',
    packages=[
        'devenv',
    ],
    package_dir={'devenv':
                 'devenv'},
    entry_points={
        'console_scripts': [
            'de=devenv.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='devenv',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
