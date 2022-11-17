import datura
import os
import pytest
import pandas as pd
import numpy as np

df = pd.DataFrame(data={'x': [1, 2],
                        'y1': [-1, 1],
                        'y2': [0, -1],
                        'y1u': [0, 3],
                        'y1l': [-2, -1]})

ar = np.array([[1, 2], [-1, 1], [0, -1], [0, 3], [-2, -1]]).T


@pytest.mark.parametrize(
    "xs,ys,yus,yls,filename_base",
    [
        ([1, 2], [-1, 1], None, None, 'one_line'),
        ([[1, 2]], [[-1, 1]], None, None, 'one_line'),
        (df['x'], df['y1'], None, None, 'one_line'),
        (ar[:, 0], ar[:, 1], None, None, 'one_line'),
        ([1, 2], [-1, 1], [0, 3], [-2, -1], 'one_patch'),
        ([[1, 2]], [[-1, 1]], [[0, 3]], [[-2, -1]], 'one_patch'),
        (df['x'], df['y1'], df['y1u'], df['y1l'], 'one_patch'),
        (ar[:, 0], ar[:, 1], ar[:, 3], ar[:, 4], 'one_patch'),
        ([1, 2], [[-1, 1], [0, -1]], None, None, 'two_lines'),
        ([[1, 2], [1, 2]], [[-1, 1], [0, -1]], None, None, 'two_lines'),
        (df['x'], df[['y1', 'y2']], None, None, 'two_lines'),
        (df[['x', 'x']], df[['y1', 'y2']], None, None, 'two_lines'),
        (ar[:, 0], ar[:, 1:3], None, None, 'two_lines'),
        (np.hstack((ar[:, :1], ar[:, :1])), ar[:, 1:3],
            None, None, 'two_lines')
    ],
)
class TestLinePlot:
    def test_basic(self, xs, ys, yus, yls, filename_base):
        this_filename_base = filename_base + '_basic'
        out_svg = os.path.join('tests', this_filename_base+'.svg')
        persistent_svg = os.path.join('tests',
                                      this_filename_base+'_persistent.svg')

        _out = datura.plot(xs, ys, yus=yus, yls=yls, filename=out_svg)
        with open(out_svg) as out_svg_file:
            with open(persistent_svg) as persistent_svg_file:
                assert out_svg_file.read() == persistent_svg_file.read()

    def test_axis_limits_from_x_ticks(self, xs, ys, yus, yls, filename_base):
        this_filename_base = filename_base + '_xlim'
        out_svg = os.path.join('tests', this_filename_base+'.svg')
        persistent_svg = os.path.join('tests',
                                      this_filename_base+'_persistent.svg')

        _out = datura.plot(xs, ys, yus=yus, yls=yls, x_ticks=[0, 1, 2, 3],
                           filename=out_svg)
        with open(out_svg) as out_svg_file:
            with open(persistent_svg) as persistent_svg_file:
                assert out_svg_file.read() == persistent_svg_file.read()

    def test_axis_limits_from_y_ticks(self, xs, ys, yus, yls, filename_base):
        this_filename_base = filename_base + '_ylim'
        out_svg = os.path.join('tests', this_filename_base+'.svg')
        persistent_svg = os.path.join('tests',
                                      this_filename_base+'_persistent.svg')
        _out = datura.plot(xs, ys, yus=yus, yls=yls, y_ticks=[0, 1, 2],
                           filename=out_svg)
        with open(out_svg) as out_svg_file:
            with open(persistent_svg) as persistent_svg_file:
                assert out_svg_file.read() == persistent_svg_file.read()
