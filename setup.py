from distutils.core import setup

setup(
    name='BrotherPrint',
    version='0.1.0',
    author='Kyle Petrovich',
    author_email='kylepetrovich@gmail.com',
    packages=['brotherprint', 'brotherprint.test'],
    url='http://github.com/fozzle/python-brotherprint',
    license='LICENSE.txt',
    description='Wrapper for Brother networked label printing commands.',
    long_description=open('README.txt').read(),
)