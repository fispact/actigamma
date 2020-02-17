from setuptools import setup


setup(name='actigamma',
      version='0.0.1',
      description='The package for producing gamma spec from nuclide activities',
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
      zip_safe=False,
      )
