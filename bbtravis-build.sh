#!/usr/bin/env bash
set -e -x

conda remove -y -n test-environment --all || :
conda create -q -n test-environment python=$TRAVIS_PYTHON_VERSION alabaster>=0.7.9 atlas cycler docopt h5py matplotlib numpy>=1.12 numpydoc>=0.5.0 pillow pygments>=2.1.0 pyqt scipy sphinx>=1.5.0 sphinx_rtd_theme>=0.1.9 six vtk

. activate test-environment

conda list
python setup.py develop

cd docs/html_docs
make html > make.out 2>&1

. deactivate
