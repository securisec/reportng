from distutils.core import setup
from setuptools import find_packages

with open('reportng/__version__.py', 'r') as f:
    exec(f.read())

setup(
    name="reportng",
    packages=find_packages(include=(["reportng"])),
    version=__version__,
    author=__author__,
    description="reportng is a simple python module that allows one to create beautiful yet simple Bootstrap 4 html reports. Reportng is capable of working with any string types output that is generated by python.",
    author_email="",
    url="https://github.com/securisec/reportng",
    keywords=["report", "reporting", "bootstrap"],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Natural Language :: English",
    ],
    install_requires=["dominate==2.4.0", "requests", "typing_extensions"],
)
