from setuptools import setup, find_packages

# Read the README file for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="piaquapulse",
    version="1.0.1",
    author="Aaron Jacobs",
    author_email="git@aaronemail.xyz",
    description="A smart water quality monitoring system for environmental research using Raspberry Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aaronjacobs-chelt/PiAquaPulse",
    project_urls={
        "Bug Reports": "https://github.com/aaronjacobs-chelt/PiAquaPulse/issues",
        "Source": "https://github.com/aaronjacobs-chelt/PiAquaPulse",
        "Documentation": "https://github.com/aaronjacobs-chelt/PiAquaPulse/blob/main/SETUP.md",
        "Circuit Design": "https://app.cirkitdesigner.com/project/9ebd3616-910c-42d6-a1ab-20e3393ac790",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8", 
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Environmental Science",
        "Topic :: System :: Hardware",
        "Topic :: System :: Monitoring",
        "Environment :: No Input/Output (Daemon)",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-mock>=3.10.0",
            "black>=22.3.0",
            "isort>=5.10.1",
            "flake8>=4.0.1",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "piaquapulse=PAPScript:main",
        ],
    },
    keywords=[
        "raspberry-pi",
        "water-quality",
        "environmental-monitoring", 
        "sensors",
        "iot",
        "data-logging",
        "research",
        "kayaking",
        "citizen-science",
    ],
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yaml", "*.yml"],
    },
    data_files=[
        ("docs", ["README.md", "SETUP.md", "CONTRIBUTING.md"]),
        ("examples", ["Circuit Documentation.md"]),
    ],
    platforms=["linux"],
    maintainer="Aaron Jacobs",
    maintainer_email="git@aaronemail.xyz",
    license="MIT",
    zip_safe=False,
)

