import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bus_data_analysis",
    version="0.0.1",
    author="Michał Korniak",
    author_email="michael.korniak@gmail.com",
    description="A package to analyze bus data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/M-Korniak/BusAnalysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

