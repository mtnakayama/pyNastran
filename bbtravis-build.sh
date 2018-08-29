#!/usr/bin/env bash
set -e -x

echo ${PATH}
echo $(ls $(echo ${PATH} | cut -d: -f1))

# . deactivate  # deactivate virtualenv

conda create -q -n test-environment python=$TRAVIS_PYTHON_VERSION || :
conda install -q -n test-environment alabaster>=0.7.9 atlas cycler docopt h5py matplotlib numpy>=1.12 numpydoc>=0.5.0 pillow pygments>=2.1.0 pyqt scipy sphinx>=1.5.0 sphinx_rtd_theme>=0.1.9 six vtk

source /buildbot/miniconda/bin/activate test-environment

conda info --envs
conda list
python setup.py develop

cd docs/html_docs

ls .

make html > make.out 2>&1

source deactivate
