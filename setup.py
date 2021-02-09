from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'med2img',
    version          = '1.1.1',
    description      = 'An app to convert medical MRI image data like DICOMs and NIFTI to readable formats like PNG/JPG',
    long_description = readme,
    author           = 'Arushi Vyas',
    author_email     = 'dev@babyMRI.org',
    url              = 'https://github.com/FNNDSC/pl-med2img',
    packages         = ['med2img'],
    install_requires = ['chrisapp'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.8',
    entry_points     = {
        'console_scripts': [
            'med2img = med2img.__main__:main'
            ]
        }
)
