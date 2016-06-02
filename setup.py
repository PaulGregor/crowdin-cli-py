# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()

with open('requirements.txt') as reqs:
    install_requires = [
        line for line in reqs.read().split('\n') if (line and not
                                                     line.startswith('--'))
    ]

setup(
    name='crowdin-cli-py',
    version='0.95.4',
    author='PaulGregor',
    author_email='comixan@gmail.com',
    packages=['crowdin'],
    include_package_data=True,
    url='https://github.com/PaulGregor/crowdin-cli',
    license='MIT',
    description='Command-line client for the crowdin.com',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Software Development :: Localization',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    zip_safe=False,
    entry_points="""
    [console_scripts]
    crowdin-cli-py = crowdin.cli:start_cli
    """,
    install_requires=install_requires,
)