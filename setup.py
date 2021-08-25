from setuptools import find_namespace_packages, setup

packages = find_namespace_packages(include=["pulpcore.cli.*"])


setup(
    name="pulp-cli-deb",
    description="Command line interface to talk to pulpcore's REST API. (Debian plugin commands)",
    version="0.0.1",
    packages=packages,
    package_data={package: ["py.typed"] for package in packages},
    python_requires=">=3.6",
    install_requires=[
        "click",
        "pulp-cli",
    ],
    entry_points={
        "pulp_cli.plugins": [
            "deb=pulpcore.cli.deb",
        ],
    },
    license="GPLv2+",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Software Distribution",
        "Typing :: Typed",
    ],
)
