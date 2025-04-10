from setuptools import setup, find_packages

setup(
    name="pyadsbdb",
    version="0.1.2",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
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
