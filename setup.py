"""
A setup module.

Partially imported from: 
https://github.com/pypa/sampleproject/blob/master/setup.py

"""

# setuptools rather than distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup (
    name='SVO_Automation',

    # The version naming scheme is the public version scheme
    # specified in PEP 440. A description of it can be found at:
    # https://packaging.python.org/distributing/#choosing-a-versioning-scheme
    #
    # a1 = alpha 1
    version='1.0.0.a1',

    description='An automatic subject-verb-object triple extraction tool for the
        social sciences.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/emoryjianghang/SVO_Automation',

    author='Alec Wolyniec, Hang Jiang, and Doris Zhou',
    author_email='alecwolyniec@gmail.com',

    # The MIT license allows users to modify the software freely
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',

        'License :: OSI Approved :: MIT License',

        # List of programming languages (including versions of Python)
        # that this project works on 
        # TODO: Make this list full and exhaustive
        # TODO: Verify that this works on Python 3.5 
        # TODO: Make the project compatible with Python 2 and 3, as PYPA recommends
        #   this (it's good practice)
        'Programming Language :: Python :: 3.6',
    ],

    keywords='text analysis data cleaning relation triples',

    # may want to exclude packages that are not to be released and installed
    packages=find_packages(),

    # TODO: Resolve the dependency on Stanford CoreNLP, as this is not a Python
    # package (dependencies can be found on the Github repository for this project)
    #
    install_requires=['nltk', 'enchant'],

    # These don't seem to be required, but these examples will be maintained:
    """
      extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
      },
    """

    # any data files that need to be included in the installation should be included
    # here, with the format given as follows:
    """
        'sample': ['package_data.dat'],
        'sample2': ['package_data2.dat'],
    """
    package_data={},

    # TODO: include Java version of Stanford CoreNLP and ClausIE here?
    # Entry format:
    """
        ('my_data', ['data/data_file'])
    """
    data_files=[],

    # Used for executable scripts with cross-platform support
    """
        entry_points={
            'console_scripts': [
                'sample=sample:main',
            ],
        },
    """
    entry_points={},
)
