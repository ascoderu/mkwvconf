from setuptools import find_packages
from setuptools import setup

with open('version.txt') as fobj:
    version = fobj.read().strip()

with open('README.rst') as fobj:
    long_description = fobj.read().strip()


setup(
    name='mkwvconf',
    version=version,
    author='Clemens Wolff',
    author_email='clemens.wolff+pypi@gmail.com',
    packages=find_packages(),
    url='https://github.com/ascoderu/mkwvconf',
    download_url='https://pypi.python.org/pypi/mkwvconf',
    scripts=['mkwvconf.py'],
    license='Apache Software License',
    description=('Automatically generate a wvdial configuration for mobile '
                 'broadband devices using mobile-broadband-provider-info'),
    long_description=long_description,
    python_requires='>=2.7.*,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities'
    ])
