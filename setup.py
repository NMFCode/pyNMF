'''setup.py'''

# pylint: disable=F0401,E0611,W0142

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import NMF
import pip

from pip.req import parse_requirements
from optparse import Option
options = Option("--workaround")
options.skip_requirements_regex = None
reqs_file = './requirements.txt'
if pip.__version__.startswith('1.'):
    install_reqs = parse_requirements(reqs_file, options=options)
else:
    from pip.download import PipSession  # pylint:disable=no-name-in-module
    options.isolated_mode = False
    install_reqs = parse_requirements(  # pylint:disable=unexpected-keyword-arg
        reqs_file,
        session=PipSession,
        options=options
    )
reqs = [str(ir.req) for ir in install_reqs]

pip.main(['install', '--no-clean', cython_req, numpy_req])

config = {
    'description': 'Python Modeling Framework',
    'author': 'Georg Hinkel',
    'author_email': 'hinkel@fzi.de',
    'version': NMF.__version__,
    'install_requires': reqs,
    'packages': ['NMF',
                 'NMF.Collections',
                 'NMF.Collections.Generic',
                 'NMF.Collections.ObjectModel',
                 'NMF.Expressions',
                 'NMF.Expressions.Linq',
                 'NMF.Models',
                 'NMF.Models.Collections',
                 'NMF.Models.Expressions',
                 'NMF.Models.Meta',
                 'NMF.Models.Repository',
                 'NMF.Serialization',
                 'NMF.Utilities',
                 'python',
                 'python.serializer'],
    'scripts': [],
    'name': 'pyNMF',
    'include_package_data': True,
}

setup(**config)
