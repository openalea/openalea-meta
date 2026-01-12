# Installation

You must use conda environment : <https://docs.conda.io/en/latest/index.html>

## Users

### Create a new environment with openalea-meta installed in there

```bash

mamba create -n openalea-meta -c openalea3 -c conda-forge  openalea.openalea-meta
mamba activate openalea-meta
```

Install openalea-meta in a existing environment

```bash
mamba install -c openalea3 -c conda-forge openalea.openalea-meta
```

### (Optional) Test your installation

```bash
mamba install -c conda-forge pytest
git clone https://github.com/openalea/openalea-meta.git
cd openalea-meta/test; pytest
```

## Developers

### Install From source

```bash
# Install dependency with conda
mamba env create -n phm -f conda/environment.yml
mamba activate openalea-meta

# Clone openalea-meta and install
git clone https://github.com/openalea/openalea-meta.git
cd openalea-meta
pip install .

# (Optional) Test your installation
cd test; pytest
```
