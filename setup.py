from setuptools import setup, find_packages
from pyadsbdb.__version__ import __version__

setup(
    name="pyadsbdb",
    version=__version__,
    packages=find_packages(exclude=["tests*"]),
    install_requires=["requests"],
    author="T.Theekshana",
    description="A Python wrapper for the adsbdb API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ttheek/pyadsbdb",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
