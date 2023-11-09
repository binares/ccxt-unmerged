import pathlib
from setuptools import setup, find_packages
import sys

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

is_python_2 = sys.version_info < (3, 0)

setup(
    name="ccxt-unmerged",
    version="4.0",
    description="Some 40 exchanges that haven't been merged into ccxt yet.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/binares/ccxt-unmerged",
    author="binares",
    author_email="binares@protonmail.com",
    packages=find_packages(
        exclude=["ccxt_unmerged.async_support*"] if is_python_2 else []
    ),
    install_requires=[
        "ccxt",
    ],
)
