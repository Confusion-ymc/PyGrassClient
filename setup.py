from distutils.core import setup

from setuptools import find_packages

with open("README.md", "r") as f:
    long_description = f.read()
setup(name='PyGrassClient',  # 包名
      version='1.0.3',  # 版本号
      description='Get Grass Python Package',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='confusion',
      author_email='1107238486@qq.com',
      url='https://github.com/Confusion-ymc/PyGrassClient',
      install_requires=[
          'websocket-client==1.7.0',
          'loguru==0.7.2',
          'python-socks==2.4.4'
      ],
      license="Apache-2.0",
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
      )

