import datura
import os
import pytest
import pandas as pd
import numpy as np

df = pd.DataFrame(data={'x':[1, 2], 'y1':[-1, 1], 'y2':[0, -1]})
ar = np.array([[1, 2], [-1, 1], [0, -1]]).T

@pytest.mark.parametrize(
    "xs,ys,filename_base",
    [
        ([1, 2], [-1, 1], 'one_line'),
        ([[1, 2]], [[-1, 1]], 'one_line'),
        (df['x'], df['y1'], 'one_line'),
        (ar[:,0], ar[:,1], 'one_line'),
        ([1, 2], [[-1, 1], [0, -1]], 'two_lines'),
        ([[1, 2], [1, 2]], [[-1, 1], [0, -1]], 'two_lines'),
        (df['x'], df[['y1', 'y2']], 'two_lines'),
        (df[['x', 'x']], df[['y1', 'y2']], 'two_lines'),
        (ar[:,0], ar[:,1:], 'two_lines'),
        (np.hstack((ar[:, :1], ar[:, :1])), ar[:,1:], 'two_lines')
    ],
)
class TestLinePlot:
    def test_basic(self, xs, ys, filename_base):
        this_filename_base = filename_base + '_basic'
        out_svg = os.path.join('tests', this_filename_base+'.svg')
        persistent_svg = os.path.join('tests', this_filename_base+'_persistent.svg')

        _out = datura.plot(xs, ys, filename=out_svg)
        with open(out_svg) as out_svg_file:
            with open(persistent_svg) as persistent_svg_file:
                assert out_svg_file.read() == persistent_svg_file.read()

    def test_axis_limits_from_x_ticks(self, xs, ys, filename_base):
        this_filename_base = filename_base + '_xlim'
        out_svg = os.path.join('tests', this_filename_base+'.svg')
        persistent_svg = os.path.join('tests', this_filename_base+'_persistent.svg')

        _out = datura.plot(xs, ys, x_ticks=[0, 1, 2, 3], filename=out_svg)
        with open(out_svg) as out_svg_file:
            with open(persistent_svg) as persistent_svg_file:
                assert out_svg_file.read() == persistent_svg_file.read()

    def test_axis_limits_from_y_ticks(self, xs, ys, filename_base):
        this_filename_base = filename_base + '_ylim'
        out_svg = os.path.join('tests', this_filename_base+'.svg')
        persistent_svg = os.path.join('tests', this_filename_base+'_persistent.svg')
        _out = datura.plot(xs, ys, y_ticks=[0, 1, 2], filename=out_svg)
        with open(out_svg) as out_svg_file:
            with open(persistent_svg) as persistent_svg_file:
                assert out_svg_file.read() == persistent_svg_file.read()
