from setuptools import setup, find_packages

setup(
    name="stockcli",
    version="1.0.0",
    description="A simple terminal application to check stock prices with charting capabilities",
    author="Stock CLI Developer",
    packages=find_packages(),
    install_requires=[
        "yfinance>=0.2.0",
        "plotext>=5.2.0",
    ],
    entry_points={
        "console_scripts": [
            "stk=stockCLI:main",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 