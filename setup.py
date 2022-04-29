from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in exotel_integration/__init__.py
from exotel_integration import __version__ as version

setup(
	name="exotel_integration",
	version=version,
	description="Exotel Integration for ERPNext",
	author="Frappe Technologies",
	author_email="suraj@frappe.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
