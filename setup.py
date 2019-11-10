import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bookmyshow-notify",
    packages=["bookmyshow-notify"],
    version="0.1.0",
    author="Sreesh Mallya",
    author_email="sreeshsmallya@gmail.com",
    description="Notifies you when a show is available on BookMyShow.",
    long_description=long_description,
    keywords="bookmyshow notify",
    long_description_content_type="text/markdown",
    url="https://github.com/sreesh-mallya/bookmyshow-notify",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU GPL",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)