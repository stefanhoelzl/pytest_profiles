"""scriptenv setup script"""

from pathlib import Path

from setuptools import setup
from tools.release import version

ProjectName = "pytest_profiles"

setup(
    name=ProjectName,
    version=version(),
    author="Stefan Hoelzl",
    author_email=f"stefanh+{ProjectName}@posteo.de",
    url="https://www.github.com/stefanhoelzl/pytest_profiles/",
    license="MIT",
    description="pytest plugin for configuration profiles",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    keywords="pytest plugin configuration config profile template",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development",
        "Topic :: Software Development :: Testing",
    ],
    packages=[ProjectName],
    install_requires=[
        "pytest>=3.7.0",
    ],
    entry_points={
        "pytest11": [
            "pytest_profiles=pytest_profiles.plugin",
        ],
    },
    zip_safe=False,
)
