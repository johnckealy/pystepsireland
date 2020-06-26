import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jokea", # Replace with your own username
    version="0.1.0",
    author="John C. Kealy",
    author_email="johnckealy.dev@gmail.com",
    description="A wrapper for pysteps adjusted for Irish rainfall",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnckealy/pystepsireland",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)