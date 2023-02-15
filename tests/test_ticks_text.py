import datura
import numpy as np
import pandas as pd
from datetime import datetime
import os


def test_default_ticks_text():

    this_fn_base = 'ticks'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.plot([1, 1000], [0, 1000], filename=out_svg)

    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()


def test_x_ticks_text():

    this_fn_base = 'ticks'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.plot([1, 1000],
                       [0, 1000],
                       filename=out_svg,
                       x_ticks=[1, 1000],
                       x_ticks_text=['one', 'one thousand'])

    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            psvg = persistent_svg_file.read()
            psvg = psvg.replace('dominant-baseline="hanging" > 1 <',
                                'dominant-baseline="hanging" > one <')
            psvg = psvg.replace('dominant-baseline="hanging" > 1K <',
                                'dominant-baseline="hanging" > one thousand <')
            assert out_svg_file.read() == psvg


def test_yticks_text():

    this_fn_base = 'ticks'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.plot([1, 1000],
                       [0, 1000],
                       filename=out_svg,
                       y_ticks=[0, 1000],
                       y_ticks_text=['zero', 'one k'])

    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            psvg = persistent_svg_file.read()
            psvg = psvg.replace('dominant-baseline="middle" > 0 <',
                                'dominant-baseline="middle" > zero <')
            psvg = psvg.replace('dominant-baseline="middle" > 1K <',
                                'dominant-baseline="middle" > one k <')
            assert out_svg_file.read() == psvg
