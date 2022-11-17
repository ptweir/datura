import datura
import numpy as np
import pandas as pd
import os


def test_fill_colors():
    rng = np.random.RandomState(10)
    ar = np.vstack((rng.normal(loc=5, scale=2, size=12),
                    rng.normal(loc=20, scale=2, size=12),
                    rng.normal(loc=35, scale=2, size=12))).T

    dts = pd.date_range(start='2022-01-01', end='2022-12-31', freq='MS')

    df = pd.DataFrame(data={'x': dts,
                            'y': ar[:, 1],
                            'yu': ar[:, 2],
                            'yl': ar[:, 0]})

    this_fn_base = 'colors'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.plot(df['x'], df['y'], yus=df['yu'], yls=df['yl'],
                       colors=['midnightblue'], fill_colors=['palegreen'],
                       fill_opacities=[0.3], filename=out_svg, y_ticks=[0, 50])
    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()


def test_many_colors():
    rng = np.random.RandomState(10)
    ar = rng.normal(loc=5, scale=2, size=12)
    labels = [5]
    for this_loc in range(6, 41):
        ar = np.vstack((ar, rng.normal(loc=this_loc, scale=2, size=12)))
        if this_loc % 5 == 0:
            labels.append(str(this_loc))
        else:
            labels.append('')
    ar = ar.T

    dts = pd.date_range(start='2022-01-01', end='2022-12-31', freq='MS')

    this_fn_base = 'many_colors'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.plot(dts, ar, filename=out_svg, labels=labels,
                       y_ticks=[0, 10, 20, 30, 40])
    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()
