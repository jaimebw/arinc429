from setuptools import setup, find_packages

setup(
    name="arinc429",
    version="0.1.0",
    description="ARINC 429 Protocol Implementation",
    author="Jaime Bowen Varela",  # TODO: Add your name
    author_email="jaimebwv@gmail.com",  # TODO: Add your email
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
