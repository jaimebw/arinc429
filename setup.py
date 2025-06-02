from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="arinc429",
    version="0.1.6",
    description="A library for working with ARINC 429 data",
    author="Jaime Bowen Varela",  
    author_email="jaimebwv@gmail.com",  
    long_description_content_type="text/markdown",
    url="https://github.com/jaimebw/arinc429",
    packages=find_packages(),
    install_requires=[
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
        ],
    },

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
    ],
    python_requires=">=3.7",
)
