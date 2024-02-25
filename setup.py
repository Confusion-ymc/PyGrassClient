import os
from distutils.core import setup

from setuptools import find_packages

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "PyGrassClient", "__version__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), about)

setup(name='PyGrassClient',  # 包名
      version=about["__version__"],  # 版本号
      description=about["__description__"],
      long_description=long_description,
      long_description_content_type='text/markdown',
      author=about["__author__"],
      author_email=about["__author_email__"],
      url=about["__url__"],
      install_requires=[
          'websocket-client==1.7.0',
          'loguru==0.7.2',
          'python-socks==2.4.4'
      ],
      license=about["__license__"],
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "License :: OSI Approved :: Apache Software License",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: 3.12",
          "Programming Language :: Python :: 3 :: Only",
          "Topic :: Software Development :: Libraries",
      ],
      project_urls={
          "Documentation": "https://github.com/Confusion-ymc/PyGrassClient",
          "Source": "https://github.com/Confusion-ymc/PyGrassClient",
      }
      )
