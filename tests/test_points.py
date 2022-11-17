import datura
import numpy as np
import pandas as pd
import os


def test_scatter_points():
    rng = np.random.RandomState(10)
    ar = np.vstack((rng.normal(loc=50, scale=10, size=100),
                    rng.normal(loc=100, scale=30, size=100),
                    rng.normal(loc=150, scale=20, size=100))).T

    xr = np.arange(1, 101)

    df = pd.DataFrame(data={'x': xr,
                            'y1': ar[:, 0],
                            'y2': ar[:, 1],
                            'y3': ar[:, 2]})

    this_fn_base = 'scatter_points'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.plot(df['x'], df[['y1', 'y2', 'y3']], line_widths=None,
                       points_radii=[1, 1.5, 2], filename=out_svg,
                       y_ticks=[0, 200], labels=['r = 1', 'r = 1.5', 'r = 2'])
    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()


def test_lines_and_scatters():
    rng = np.random.RandomState(10)
    ar = np.vstack((rng.normal(loc=0, scale=10, size=101),
                    rng.normal(loc=0, scale=30, size=101))).T

    xr = np.arange(-50, 51)

    data = {'x1': xr.tolist(), 'x2': xr.tolist(),
            'x3': [-50, 50], 'x4': [-50, 50],
            'y1': (ar[:, 0] + xr).tolist(), 'y2': (ar[:, 1] + 2 * xr).tolist(),
            'y3': [-50, 50], 'y4': [-100, 100]}

    this_fn_base = 'lines_and_scatters'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.plot([data['x1'], data['x2'], data['x3'], data['x4']],
                       [data['y1'], data['y2'], data['y3'], data['y4']],
                       line_widths=[0, 0, 1, 1],
                       points_radii=[1, 1, 0, 0], filename=out_svg,
                       x_ticks=[-50, 0, 50], y_ticks=[-100, 0, 100],
                       colors=['black', 'blue', 'black', 'blue'])
    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()
