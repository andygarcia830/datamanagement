from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in datamanagement/__init__.py
from datamanagement import __version__ as version

setup(
	name="datamanagement",
	version=version,
	description="Data Management",
	author="Andy Garcia",
	author_email="andy@xurpas.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
