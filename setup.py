from setuptools import setup

# reading long description from file
with open('DESCRIPTION.txt') as file:
    long_description = file.read()

# specify requirements of your package here
REQUIREMENTS = ['requests','netjsonconfig', 'flask']

# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
]

# calling the setup function
setup(name='netjson-rest',
      version='1.0.0',
      description='A rest API to convert openwrt config to json and vice versa using flask',
      long_description=long_description,
      url='https://github.com/umeshahp/netjson-rest',
      author='Umesha HP',
      author_email='hpu89@yahoo.com',
      license='MIT',
      packages=['netjsonFlaskRest'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='Rest API for netjson config'
      )
