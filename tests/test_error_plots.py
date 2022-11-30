import datura
import numpy as np
import pandas as pd
import os


def test_error_plot_symmetrical():
    xs = [-1, 2]
    ys = [[0, 0], [4, 5]]
    y_errors = [[1, .5], [2, 3]]

    this_fn_base = 'symmetrical_error'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.error_plot(xs, ys,
                             y_errors=y_errors, filename=out_svg,
                             y_ticks=[-1, 0, 1, 2, 3, 4, 5, 6, 7, 8])
    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()


def test_error_plot():
    xs = [-1, 2]
    ys = [[0, 0], [4, 5]]
    yus = [[1, .5], [6, 8]]
    yls = [[-1, -.5], [2, 2]]

    this_fn_base = 'symmetrical_error'
    out_svg = os.path.join('tests', this_fn_base+'.svg')
    persistent_svg = os.path.join('tests', this_fn_base+'_persistent.svg')

    _out = datura.error_plot(xs, ys,
                             yus=yus, yls=yls, filename=out_svg,
                             y_ticks=[-1, 0, 1, 2, 3, 4, 5, 6, 7, 8])
    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()
