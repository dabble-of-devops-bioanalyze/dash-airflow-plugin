#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as f:
    requirements = f.readlines()

requirements = [x.strip() for x in requirements]
requirements = []

setup_requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Jillian Rowe",
    author_email='jillian@dabbleofdevops.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Dash Airflow Plugin contains contains helper functions to create blueprints and render webpages with Dash.",
    entry_points={
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='dash_airflow_plugin',
    name='dash_airflow_plugin',
    packages=find_packages(include=['dash_airflow_plugin', 'dash_airflow_plugin.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/dabble-of-devops-bioanalyze/dash_airflow_plugin',
    version='0.1.0',
    zip_safe=False,
)
