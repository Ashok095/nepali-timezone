from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nepali-timezone",
    version="0.1.0",
    author="Ashok Dhakal",
    author_email="info@ashokdhakal.com",
    description="A Django package for handling Nepali (Bikram Sambat) dates and times with timezone awareness",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ashok095/nepali-timezone",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
        "nepali-datetime>=1.0.0",
        "pytz>=2021.1",
        "python-dateutil>=2.8",
        "djangorestframework>=3.12",
    ],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)