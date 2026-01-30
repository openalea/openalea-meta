# openalea-meta

_________________

[![Build Status](https://github.com/openalea/openalea-meta/actions/workflows/openalea_ci.yml/badge.svg)](https://github.com/openalea/openalea-meta/actions/workflows/openalea_ci.yml)
[![License](https://img.shields.io/badge/License--CeCILL-C-blue)](https://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html)
[![Anaconda-Server Badge](https://anaconda.org/openalea3/openalea-meta/badges/version.svg)](https://anaconda.org/openalea3/openalea-meta)

_________________

**openalea-meta** is an openalea meta-package that allows to install with one command line the stable release. The following 
openalea packages are included:
  - [openalea.plantgl 3.22.3](https://plantgl.readthedocs.io/en/stable/)
  - [openalea.lpy 3.15.4](https://lpy.readthedocs.io/en/stable/)
  - [openalea.core 2.5.0](https://github.com/openalea/core)
  - [openalea.widgets 1.1.2](https://oawidgets.readthedocs.io/en/stable/)
  - [openalea.mtg 2.3.0](https://mtg.readthedocs.io/en/stable/)
  - [openalea.scipack 2.5.2](https://scipack.readthedocs.io/en/stable/)
  - [openalea.oalab 2.5.0](https://github.com/openalea/oalab)
  - [openalea.grapheditor 2.5.0](https://grapheditor.readthedocs.io/en/stable/)
  - [openalea.visualea 2.5.0](https://visualea.readthedocs.io/en/stable/)
  - [openalea.weberpenn 2.5.0](https://openalea.readthedocs.io/en/stable/tutorials/visualea/weberpenn.html)
  - [openalea.rsml 1.5.0](https://rsml.readthedocs.io/en/stable/)
  - [openalea.caribu 8.2.1](https://caribu.readthedocs.io/en/stable/)
  - [openalea.astk 3.1.0](https://openalea-astk.readthedocs.io/)
  - [openalea.adel 2.1.1](https://adel.readthedocs.io/en/stable/)
  - [openalea.spice 1.1.1](https://openalea-spice.readthedocs.io/en/stable/)
  - [openalea.hydroroot 2.1.0](https://hydroroot.readthedocs.io/en/stable/)
  - [openalea.phenomenal 1.10.4](https://phenomenal.readthedocs.io/en/stable/)
  - [openalea.hydroshoot 5.3.0](https://hydroshoot.readthedocs.io/en/stable/)
  - [openalea.ratp 2.2.0](https://pyratp.readthedocs.io/en/stable/)


### Installation
```bash
mamba create -n openalea -c openalea3 -c conda-forge openalea
```

The environement and the package can be installed also as follows:
```bash
mamba env create -f conda/environment.yml
```

### Documentation
A general documentation on openalea can be found [here](https://openalea.readthedocs.io/en/stable/index.html). Documentation
of each package can be found following the links above.

### Contributors

Thanks to all that contribute making this package what it is !

<a href="https://github.com/openalea/openalea-meta/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=openalea/openalea-meta" />
</a>
