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
    packages=['mkwvconf'],
    url='https://github.com/ascoderu/mkwvconf',
    download_url='https://pypi.python.org/pypi/mkwvconf',
    entry_points={
        'console_scripts': [
            'mkwvconf = mkwvconf.mkwvconf:cli',
        ],
    },
    license='Apache Software License',
    description=('Automatically generate a wvdial configuration for mobile '
                 'broadband devices using mobile-broadband-provider-info'),
    long_description=long_description,
    python_requires='>=3.12',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Utilities'
    ])
