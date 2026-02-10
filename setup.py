from setuptools import setup, find_packages
setup(name="cred-stuff", version="2.0.0", author="bad-antics", description="Credential stuffing attack simulation and defense", packages=find_packages(where="src"), package_dir={"":"src"}, python_requires=">=3.8")
