from pathlib import Path
from setuptools import Command, find_packages, setup
from shutil import copy, copytree, rmtree
from src.govcookiecutter import __version__
import subprocess
import sys

# Define a description for this package
PACKAGE_DESCRIPTION = (
    "A cookiecutter template for analytical, Python-, or Python and R-based projects "
    "within Her Majesty's Government, and wider public sector."
)

# Define the path to the parent directory of this file
dir_parent = Path(__file__).resolve().parent

# Try to parse the `README.md` file to generate the long description of this package
try:
    with open(dir_parent.joinpath("README.md"), encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = PACKAGE_DESCRIPTION

# Define paths to the template folder, and the `src` directories
dir_template = dir_parent.joinpath("{{ cookiecutter.repo_name }}")
dir_govcookiecutter = dir_parent.joinpath("src", "govcookiecutter", "govcookiecutter")
dir_govcookiecutter_template = dir_govcookiecutter.joinpath(
    "{{ cookiecutter.repo_name }}"
)

# Define a dictionary of files and folders to copy to a skeleton `govcookiecutter`
# Python package, where the keys are the current locations, and values are the
# locations within the skeleton package
copy_folders_and_files = {
    dir_parent.joinpath("hooks"): dir_govcookiecutter.joinpath("hooks"),
    dir_template: dir_govcookiecutter_template,
    dir_parent.joinpath("cookiecutter.json"): dir_govcookiecutter.joinpath(
        "cookiecutter.json"
    ),
}


class BuildPackage(Command):
    """Build a skeleton ``govcookiecutter`` package."""

    description = "Build a skeleton `govcookiecutter` package."
    user_options = []

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

    @staticmethod
    def run() -> None:
        """Build a skeleton ``govcookiecutter`` package.

        The skeleton package contains only the necessary files and folders to generate
        a project template. It also contains a CLI interface, where invoking the
        ``govcookiecutter`` command in your terminal creates the project.

        Returns:
            A universal source and wheel distribution of the skeleton `govcookiecutter`
            package.

        """

        # If they already exist, delete certain folders related to the package build
        rmtree(dir_parent.joinpath("build"), ignore_errors=True)
        rmtree(dir_parent.joinpath("dist"), ignore_errors=True)
        rmtree(dir_govcookiecutter, ignore_errors=True)

        # Copy files and folders required by `cookiecutter` to create the project
        # templates
        for k, v in copy_folders_and_files.items():
            if k.is_file():
                copy(k, v)
            elif k.is_dir():
                copytree(k, v)
            else:
                raise RuntimeError(f"Invalid file/folder to copy: {k}")

        # Create the universal source and wheel distributions
        subprocess.run(
            [sys.executable, "setup.py", "sdist", "bdist_wheel", "--universal"]
        )


# Set up the package
setup(
    name="govcookiecutter",
    version=__version__,
    description=PACKAGE_DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ukgovdatascience",
    author_email="gds-data-science@digital.cabinet-office.gov.uk",
    python_requires=">=3.6.1",
    url="https://github.com/ukgovdatascience/govcookiecutter",
    install_requires=["click", "cookiecutter"],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    entry_points={
        "console_scripts": ["govcookiecutter=govcookiecutter.__main__:main"],
    },
    cmdclass={
        "build_package": BuildPackage,
    },
)
