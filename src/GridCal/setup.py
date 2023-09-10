"""
A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import distutils.command.build
import os
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

from GridCal.__version__ import __GridCal_VERSION__


# Override build command
class BuildCommand(distutils.command.build.build):
    def initialize_options(self):
        distutils.command.build.build.initialize_options(self)
        self.build_base = 'build_gridcal'


here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
# if os.path.exists(os.path.join(here, 'README.md')):
#     with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
#         long_description = f.read()
#         print(long_description)
# else:
#     long_description = ''

long_description = '''# GridCal

This software aims to be a complete platform for power systems research and simulation.

[Watch the video https](https://youtu.be/SY66WgLGo54)

[Check out the documentation](https://gridcal.readthedocs.io)


## Installation

pip install GridCal

For more options (including a standalone setup one), follow the
[installation instructions]( https://gridcal.readthedocs.io/en/latest/getting_started/install.html)
from the project's [documentation](https://gridcal.readthedocs.io)
'''

# if os.path.exists(os.path.join(here, 'about.txt')):
#     with open(os.path.join(here, 'about.txt'), encoding='utf-8') as f:
#         description = f.read()
#         print(description)
# else:
#     description = ''
#     print('Unable to read the description file')
description = 'GridCal is a Power Systems simulation program intended for professional use and research'

base_path = os.path.join('GridCal')

pkgs_to_exclude = ['docs', 'research', 'research.*', 'tests', 'tests.*', 'Tutorials', 'GridCalEngine']

packages = find_packages(exclude=pkgs_to_exclude)


# ... so we have to do the filtering ourselves
packages2 = list()
for package in packages:
    elms = package.split('.')
    excluded = False
    for exclude in pkgs_to_exclude:
        if exclude in elms:
            excluded = True

    if not excluded:
        packages2.append(package)


package_data = {'GridCal': ['*.md',
                            '*.rst',
                            'LICENSE.txt',
                            'data/cables.csv',
                            'data/transformers.csv',
                            'data/wires.csv'],
                }

dependencies = ['setuptools>=41.0.1',
                'wheel>=0.37.2',
                "PySide6>=5.15",  # 5.14 breaks the UI generation for development
                "numpy>=1.19.0",
                "scipy>=1.0.0",
                "networkx>=2.1",
                "pandas>=1.0",
                "ortools>=9.0.0",
                "xlwt>=1.3.0",
                "xlrd>=1.1.0",
                "matplotlib>=2.1.1",
                "qtconsole>=4.5.4",
                "openpyxl>=2.4.9",
                "chardet>=3.0.4",  # for the psse files character detection
                "scikit-learn>=0.18",
                "geopy>=1.16",
                "pytest>=3.8",
                "h5py>=2.9.0",
                "numba>=0.46",  # to compile routines natively
                'pyproj',
                'pyarrow',
                'ortools',
                "darkdetect",
                "pyqtdarktheme",
                "nptyping",
                "windpowerlib",
                "pvlib",
                "hyperopt",
                "GridCalEngine==" + __GridCal_VERSION__,  # the GridCalEngine version must be exactly the same
                ]

extras_require = {
        'gch5 files':  ["tables"]  # this is for h5 compatibility
    }
# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='GridCal',  # Required
    version=__GridCal_VERSION__,  # Required
    license='LGPL',
    description=description,  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/SanPen/GridCal',  # Optional
    author='Santiago Peñate Vera et. Al.',  # Optional
    author_email='santiago@gridcal.org',  # Optional
    classifiers=[
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='power systems planning',  # Optional
    packages=packages2,  # Required
    include_package_data=True,
    python_requires='>=3.10',
    install_requires=dependencies,
    extras_require=extras_require,
    package_data=package_data,
    cmdclass={"build": BuildCommand},
)
