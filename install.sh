#!/bin/bash

# Create conda environment from environment.yml
conda env create -f environment.yml

# Activate the environment
conda activate atlas-quicklook

# Install the package in development mode
pip install -e .

echo "Environment created and package installed!"
echo "Activate with: conda activate atlas-quicklook"
