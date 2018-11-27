import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "qemu-composer",
    version = "0.0.1",
    author = "Guilherme Lunhani",
    author_email = "lunhanig@gmail.com",
    description = "Compose multiple architetures for a one-time cross-compilation",
    keywords = "docker-compose docker qemu cross-compilation",
    url = "http://packages.python.org/qemu-composer",
    install_requires=['pyyaml'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: BSD License",
    ],
    entry_points = {
        'console_scripts': [
            'qemu-composer = qemu_composer.__main__:main'
        ]
    }
)
