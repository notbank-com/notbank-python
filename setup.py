import os
import sys
import setuptools
from setuptools.command.test import test as TestCommand


CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 7)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
        ==========================
        Unsupported Python version
        ==========================
        This version of Chunked String Serde requires at least Python {}.{}, but
        you're trying to install it on Python {}.{}. To resolve this,
        consider upgrading to a supported Python version.
        """.format(
            *(REQUIRED_PYTHON + CURRENT_PYTHON),
        )
    )
    sys.exit(1)


# "setup.py publish" shortcut.
if sys.argv[-1] == "publish":
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


with open("requirements.txt", "r", encoding="utf-8") as requeriments:
    REQUIREMENTS = requeriments.readlines()


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from multiprocessing import cpu_count

            self.pytest_args = ["-n", str(cpu_count()), "--boxed"]
        except (ImportError, NotImplementedError):
            self.pytest_args = ["-n", "1", "--boxed"]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


test_requirements = [
    "pytest ==7.3.1",
]

setuptools.setup(
    name="notbank",
    version="2.3.0a1",
    packages=[
        "notbank_python_sdk",
        "notbank_python_sdk.core",
        "notbank_python_sdk.models",
        "notbank_python_sdk.requests_models",
        "notbank_python_sdk.rest",
        "notbank_python_sdk.websocket",
        "notbank_python_sdk.websocket.websocket_restarter",
    ],
    include_package_data=True,
    description="Notbank API client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[
        "api", "notbank", "cryptomkt",
        "cryptomarket", "bitcoin", "client", "cryptocurrency"],
    url="https://github.com/notbank-exchange/notbank-python",
    author="Notbank",
    python_requires=">=3.7",
    install_requires=REQUIREMENTS,
    cmdclass={"test": PyTest},
    tests_require=test_requirements,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
