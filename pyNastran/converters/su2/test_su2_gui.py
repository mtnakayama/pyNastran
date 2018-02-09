import os
import warnings
import unittest

import numpy as np
from pyNastran.utils.log import get_logger
warnings.simplefilter('always')
np.seterr(all='raise')


from pyNastran.gui.testing_methods import FakeGUIMethods
from pyNastran.converters.su2.su2_io import SU2_IO
import pyNastran

pkg_path = pyNastran.__path__[0]
model_path = os.path.join(pkg_path, 'converters', 'su2')


class SU2_GUI(FakeGUIMethods):
    def __init__(self):
        FakeGUIMethods.__init__(self)
        self.model = SU2_IO(self)


class TestSU2GUI(unittest.TestCase):

    def test_su2_geometry(self):
        log = get_logger(level='warning')
        geometry_filename = os.path.join(model_path, 'mesh_naca0012_inv.su2')

        test = SU2_GUI()
        test.log = log
        test.model.load_su2_geometry(geometry_filename)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()

