import io
import os
import setuptools


def read_description():
    url = "README.md"
    """ Read and Return the description """
    return io.open(
        os.path.join(os.path.dirname(__file__), url), encoding="utf-8"
    ).read()


def def_requirements():
    """Check PIP Requirements"""
    with open("requirements.txt", encoding="utf-8") as file_content:
        pip_lines = file_content.read().splitlines()
    return pip_lines


setuptools.setup(
    name="rion",
    version="v0.2.1",
    description="Package Manager CLI",
    entry_points={"console_scripts": ["rion=rion:handler"]},
    data_files=[("man/man1", ["man/rion.1"])],
    long_description=read_description(),
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="Package Manager CLI - rion",
    url="https://github.com/Riffecs/rion",
    packages=["rion"],
    install_requires=def_requirements(),
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
