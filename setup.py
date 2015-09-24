from distutils.core import setup

setup(
    name='brotherprint',
    version='0.1.2',
    author='Kyle Petrovich',
    author_email='kylepetrovich@gmail.com',
    packages=['brotherprint', 'brotherprint.test'],
    url='http://github.com/fozzle/python-brotherprint',
    license='LICENSE.txt',
    description='Wrapper for Brother networked label printing commands.',
    long_description=open('README.md').read(),
)
