from setuptools import setup, find_packages


setup(
    name="gviewer",
    version="1.0.0",
    description="General Viewer",
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
        "Topic :: Security",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: Software Development :: Testing"
    ],
    packages=find_packages(include=["gviewer", "gviewer.*"]),
    install_requires=[
        "urwid==1.3.1"
    ]
)
