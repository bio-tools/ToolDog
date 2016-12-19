from setuptools import setup
from pip.req import parse_requirements
import sys, os

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist bdist_wheel upload; git push")
    sys.exit()

setup(name="tooldog",
        version='0.1.0',
        description='Tool description generator (from https//bio.tools to XML)',
        author='Kenzo-Hugo Hillion',
        author_email='kehillio@pasteur.Fr',
        dependency_links=['git+https://github.com/erasche/galaxyxml#egg=galaxyxml'],
        install_requires=['requests','galaxyxml'],
        packages=["tooldog"],
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
            'Operating System :: OS Independent',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Environment :: Console',
            ],
        )
