import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
   name='ccxt-unmerged',
   version='1.0',
   description="Some 40 exchanges that haven't been merged into ccxt yet.",
   long_description=README,
   long_description_content_type='text/markdown',
   url='https://github.com/binares/ccxt-unmerged',
   author='binares',
   author_email='binares@protonmail.com',
   packages=find_packages(),
   # 3.5.3 is required by aiphttp>=3.0, which in turn
   # is required by ccxt
   python_requires='>=3.5.3',
   install_requires=[
       'ccxt',
   ],
)

