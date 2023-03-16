import datura
import numpy as np
import pandas as pd
from datetime import datetime
import os


def test_multiline_titles():

    this_fn_base = 'multiline_title'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.plot([[1], [1, 2], [1, 2, 3]],
                       [[10], [5, 10], [2, 10, 3]],
                       x_ticks=[0, 1, 2, 3, 4],
                       points_radii=5,
                       labels=['short', 'medium', 'long'],
                       title='First title line\nSecond title line',
                       filename=out_svg)

    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()
