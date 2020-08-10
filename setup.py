import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neosensory-python",
    version="0.0.1",
    author="Scott Novich",
    author_email="novich@neosensory.com",
    description="A package to help developers interact with Neosensory products",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/neosensory/neosensory-sdk-for-python",
    packages=setuptools.find_packages(),
    install_requires=['bleak'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires='>=3.6',
)