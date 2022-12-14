import os
from setuptools import setup


VERSION = ""
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.VERSION'), 'rt') as vfile:
      VERSION = vfile.readlines()[0].strip("\n").strip()

setup(name='actigamma',
      version=VERSION,
      description='The package for producing gamma spec from nuclide activities',
      long_description_content_type='text/x-rst',
      long_description='The package for producing gamma spec from nuclide activities',
      url='https://github.com/fispact/actigamma',
      author='UKAEA',
      author_email='thomas.stainer@ukaea.uk',
      license='Apache License 2.0',
      packages=[
            'actigamma',
      ],
      install_requires=[],
      python_requires='>=3',
      scripts=[],
      setup_requires=[
            'pytest-runner',
      ],
      test_suite='tests.testsuite',
      tests_require=[
            'pytest',
            'pytest-cov>=2.3.1',
            'mock',
            'numpy',
      ],
      include_package_data=True,
      zip_safe=False,
      )
