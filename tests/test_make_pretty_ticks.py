import datura
import numpy as np
import pandas as pd
from datetime import datetime
import os


def test_num2pretty_string():

    in_outs = [[0, '0'], [-10, '-10'], [10000, '10K'], [2e9, '2B']]
    for in_out in in_outs:
        _out = datura.draw._num2pretty_string(in_out[0])
        assert _out == in_out[1]


def test_check_equally_spaced():

    in_outs = [[[[1, 2, 3], [3, 4, 5], [1, 2]], True, [1, 2, 3, 4, 5]],
               [[[1, 2, 3], [3, 5], [1, 2]], False, [1, 2, 3, 5]]
               ]
    for in_out in in_outs:
        _out_1, _out_2 = datura.draw._check_equally_spaced(in_out[0])
        assert (_out_1, _out_2) == (in_out[1], in_out[2])


def test_year_ticks():
    time_range = pd.date_range(start='2010-01-01', end='2020-01-01', freq='YS')
    df = pd.DataFrame(data={'t': time_range,
                            'y1': np.sin(np.linspace(0, 2*np.pi, 11)),
                            'y2': np.cos(np.linspace(0, 4*np.pi, 11))})

    this_fn_base = 'year_ticks'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.plot(df['t'], df[['y1', 'y2']], filename=out_svg)

    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()


def test_month_ticks():
    time_range = pd.date_range(start='2023-01-01', end='2024-01-01', freq='MS')
    df = pd.DataFrame(data={'t': time_range,
                            'y1': np.sin(np.linspace(0, 2*np.pi, 13)),
                            'y2': np.cos(np.linspace(0, 4*np.pi, 13))})

    this_fn_base = 'month_ticks'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.plot(df['t'], df[['y1', 'y2']], filename=out_svg)

    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()


def test_week_ticks():
    time_range = pd.date_range(start="2023-01-01", end="2024-01-01", freq="W")
    df = pd.DataFrame(data={'t': time_range,
                            'y1': np.sin(np.linspace(0, 2*np.pi, 53)),
                            'y2': np.cos(np.linspace(0, 4*np.pi, 53))})

    this_fn_base = 'week_ticks'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.plot(df['t'], df[['y1', 'y2']], filename=out_svg)

    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()


def test_day_ticks():
    time_range = pd.date_range(start="2023-08-01", end="2023-09-01", freq="D")
    df = pd.DataFrame(data={'t': time_range,
                            'y1': np.sin(np.linspace(0, 2*np.pi, 32)),
                            'y2': np.cos(np.linspace(0, 4*np.pi, 32))})

    this_fn_base = 'day_ticks'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.plot(df['t'], df[['y1', 'y2']], filename=out_svg)

    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()


def test_hour_ticks_subday():
    time_range = pd.date_range(start="2023-08-01", end="2023-08-01 12:0:0",
                               freq="H")
    df = pd.DataFrame(data={'t': time_range,
                            'y1': np.sin(np.linspace(0, 2*np.pi, 13)),
                            'y2': np.cos(np.linspace(0, 4*np.pi, 13))})

    this_fn_base = 'hour_ticks_subday'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.plot(df['t'], df[['y1', 'y2']], filename=out_svg)

    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()


def test_hour_ticks():
    time_range = pd.date_range(start="2023-08-01", end="2023-08-02 12:0:0",
                               freq="H")
    df = pd.DataFrame(data={'t': time_range,
                            'y1': np.sin(np.linspace(0, 2*np.pi, 37)),
                            'y2': np.cos(np.linspace(0, 4*np.pi, 37))})

    this_fn_base = 'hour_ticks'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.plot(df['t'], df[['y1', 'y2']], filename=out_svg)

    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()


def test_problem1_ticks():
    ys = [[0.440795, 0.411026, 0.386452],
          [0.404519, 0.363246, 0.334465, 0.346549]]
    this_fn_base = 'problem1_ticks'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.plot(ys, filename=out_svg)

    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()


def test_problem2_ticks():

    y_s = [[0.010787,
            0.013945,
            0.015417,
            0.016254,
            0.016887,
            0.017489,
            0.018125,
            0.019201,
            0.019665,
            0.019931,
            0.021362,
            0.024205],
           [0.023771,
            0.024023,
            0.024175,
            0.023459,
            0.022641,
            0.022451,
            0.022464,
            0.022491,
            0.022484,
            0.023448,
            0.024961,
            0.026751],
           [0.027537, 0.027649]]

    this_fn_base = 'problem2_ticks'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.plot(y_s, filename=out_svg)

    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()
