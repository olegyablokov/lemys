from distutils.core import setup
from setuptools import find_packages

setup(name='lemys',
      version='0.1',
      description='a console program for learning languages',
      author='Oleg Yablokov',
      author_email='oyyablokov@gmail.com',
      url='None',
      packages=find_packages(),
      install_requires=[
          'numpy',
          'pandas',
          'requests',
          'matplotlib']
     )
