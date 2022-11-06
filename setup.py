from distutils.core import setup
from setuptools import find_packages
import susubotlib

setup(
    name='susubotlib',
    version=susubotlib.__version__,
    packages=find_packages(),
    url='https://susu.ru/',
    license='MIT',
    author='Roman',
    author_email='summedjesters@gmail.com',
    description='Test lib',
    include_package_data=True
)
