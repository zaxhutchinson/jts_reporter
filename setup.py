import os.path
from setuptools import setup

dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(dir, "README.md")) as fid:
    README = fid.read()

setup(
    name="jts-reporter",
    version=0.02,
    description="A data viz project for JTS games.",
    long_description="README",
    long_description_content_type="text/markdown",
    url="https://github.com/zaxhutchinson/jts_reporter.git",
    author="zax",
    author_email="zaxhutchinson@gmail.com",
    license="MIT",
    packages=["jtsr"],
    include_package_data=True,
    install_requires=[],
    entry_points={"console_scripts": ["jtsr=jtsr.__main__:main"]}
)
