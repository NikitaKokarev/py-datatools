from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

# requirements = []

setup(
    name="py_datatools",
    version="1.0",
    author="Nikita Kokarev",
    author_email="kokarevnickita@gmail.com",
    description="Helper functions",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/NikitaKokarev/py-datatools/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ]
)
