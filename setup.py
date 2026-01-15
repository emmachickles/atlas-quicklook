from setuptools import setup, find_packages

setup(
    name="atlas-quicklook",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "astropy",
    ],
    extras_require={
        "dev": ["jupyter", "ipython"],
    },
)
