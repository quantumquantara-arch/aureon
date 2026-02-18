# setup.py

from setuptools import setup, find_packages

setup(
    name="aureon-wormhole-channel",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    description=(
        "Aureon’s internal wormhole-coherence module — fidelity geometry, "
        "?-vector routing, coherence tunnels, and protected lattice traversal "
        "for the Aureon OS."
    ),
    author="Aureon Planetary OS",
    license="MIT",
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Distributed Computing",
    ],
)
