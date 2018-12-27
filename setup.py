from setuptools import setup

setup(
    name='mooshimeter',
    version='0.1.0',
    packages=['mooshimeter', 'mooshimeter.vendor'],
    url='https://github.com/spyoungtech/Mooshimeter-PythonAPI',
    license='GPLv3',
    author='James Whong',
    author_email='hello@moosh.im',
    maintainer='Spencer Young',
    maintainer_email='spencer.young@spyoung.com',
    description='UNOFFICIAL! This package is a fork from the original mooshimeter python API',
    install_requires=['pyserial']
)
