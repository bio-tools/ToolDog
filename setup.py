from setuptools import setup
import sys, os

import tooldog

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist bdist_wheel upload; git push")
    sys.exit()

setup(name="tooldog",
        version=tooldog.version,
        description='Tool description generator (from https//bio.tools to XML and CWL)',
        author='Kenzo-Hugo Hillion and Hervé Ménager',
        author_email='kehillio@pasteur.fr and hmenager@pasteur.fr',
        license='MIT',
        keywords = ['biotools','galaxy','xml','cwl'],
        install_requires=['ontospy==1.7.3', 'requests', 'galaxyxml', 'cwlgen>=0.1'],
        dependency_links = ['https://github.com/common-workflow-language/python-cwlgen/archive/master.zip#egg=cwlgen-0.1','https://github.com/khillion/galaxyxml/archive/master.zip#egg=galaxyxml-0.3.3'],
        packages=["tooldog"],
        package_data={
        'tooldog': ['data/*.json', 'data/*.owl'],
        },
        entry_points={'console_scripts':['tooldog=tooldog.main:run']},
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
            'Operating System :: OS Independent',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Environment :: Console',
            ],
        )
