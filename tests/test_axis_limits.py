import datura

def test_axis_limits_from_x_ticks():
    svg_out = datura.plot([1, 2], [-1, 1], x_ticks=[0, 1, 2, 3])
    assert svg_out.split('points="')[1].split('"')[0] == '146.66666666666666,174.0 253.33333333333331,26.0 '

def test_axis_limits_from_x_ticks():
    svg_out = datura.plot([1, 2], [-1, 1], y_ticks=[0, 1, 2])
    assert svg_out.split('points="')[1].split('"')[0] == '40.0,174.0 360.0,75.33333333333334 '