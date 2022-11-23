import datura
import numpy as np
import pandas as pd
import os

rng = np.random.RandomState(10)
ar = np.vstack((rng.normal(loc=-2, scale=1.5, size=5000),
                rng.normal(loc=0, scale=2, size=5000),
                rng.normal(loc=3, scale=1.5, size=5000))).T
df = pd.DataFrame(data={'yb': ar[:, 0],
                        'yy': ar[:, 1],
                        'yg': ar[:, 2]})


def test_np_hist():

    this_fn_base = 'hist'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.hist(data=ar, bin_edges=np.linspace(-10, 10, 100),
                       filename=out_svg,
                       x_label='Days until ready to eat',
                       y_label='Number of bananas',
                       colors=['brown', 'gold', 'green'],
                       labels=['brown', 'yellow', 'green'],
                       label_nudges=[0, 10, 20],
                       x_ticks=[-10, -5, 0, 5, 10],
                       y_ticks=[0])
    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()


def test_autobin_hist():

    this_fn_base = 'autobin_hist'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.hist(data=[[2 for i in range(10)],
                              list(range(10)),
                              [0 for i in range(5)]+[9 for i in range(5)]],
                       bin_edges=10, y_ticks=[0, 5, 10], filename=out_svg)
    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()


def test_autobin_hist_2():

    this_fn_base = 'autobin_hist'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.hist(data=[[2 for i in range(10)],
                              list(range(10)),
                              [0 for i in range(5)]+[9 for i in range(5)]],
                       y_ticks=[0, 5, 10], filename=out_svg)
    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()


def test_df_hist():

    this_fn_base = 'hist'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.hist(data=df[['yb', 'yy', 'yg']],
                       bin_edges=np.linspace(-10, 10, 100),
                       filename=out_svg,
                       x_label='Days until ready to eat',
                       y_label='Number of bananas',
                       colors=['brown', 'gold', 'green'],
                       labels=['brown', 'yellow', 'green'],
                       label_nudges=[0, 10, 20],
                       x_ticks=[-10, -5, 0, 5, 10],
                       y_ticks=[0])
    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()
