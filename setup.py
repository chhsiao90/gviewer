from setuptools import setup, find_packages
from codecs import open
import os


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="gviewer",
    version="2.1.3",
    description="General Viewer",
    long_description=long_description,
    author="chhsiao90",
    author_email="chhsiao90@gmail.com",
    url="https://github.com/chhsiao90/gviewer",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Environment :: Console :: Curses",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Widget Sets"
    ],
    packages=find_packages(include=["gviewer", "gviewer.*"]),
    test_suite="gviewer.tests",
    install_requires=[
        "urwid==1.3.1"
    ],
    extras_require={
        "dev": [
            "Pygments==2.1.3",
            "mock==2.0.0"
        ]
    }
)
