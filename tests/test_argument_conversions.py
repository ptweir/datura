import datura
import numpy as np
import pandas as pd

def test_lists_one_x_one_y_column():
    svg_out = datura.plot([1, 2], [-1, 1])
    assert svg_out.split('points="')[1].split('"')[0] == '40.0,174.0 360.0,26.0 '

def test_lists_one_x_two_y_column():
    svg_out = datura.plot([1, 2], [[-1, 1], [2, 1]])
    assert svg_out.split('points="')[1].split('"')[0] == '40.0,174.0 360.0,75.33333333333334 '

def test_pd_one_x_one_y_column():
    df = pd.DataFrame(data={'x':[1, 2], 'y1':[-1, 1], 'y2':[2, 1]})
    svg_out = datura.plot(df['x'], df['y1'])
    assert svg_out.split('points="')[1].split('"')[0] == '40.0,174.0 360.0,26.0 '

def test_pd_one_x_two_y_column():
    df = pd.DataFrame(data={'x':[1, 2], 'y1':[-1, 1], 'y2':[2, 1]})
    svg_out = datura.plot(df['x'], df[['y1','y2']])
    assert svg_out.split('points="')[1].split('"')[0] == '40.0,174.0 360.0,75.33333333333334 '

def test_pd_two_x_two_y_column():
    df = pd.DataFrame(data={'x':[1, 2], 'y1':[-1, 1], 'y2':[2, 1]})
    svg_out = datura.plot(df[['x', 'x']], df[['y1','y2']])
    assert svg_out.split('points="')[1].split('"')[0] == '40.0,174.0 360.0,75.33333333333334 '

def test_np_one_x_one_y_column():
    ar = np.array([[1, 2], [-1, 1], [2, 1]]).T
    svg_out = datura.plot(ar[:,0], ar[:,1])
    assert svg_out.split('points="')[1].split('"')[0] == '40.0,174.0 360.0,26.0 '

def test_np_one_x_two_y_column():
    ar = np.array([[1, 2], [-1, 1], [2, 1]]).T
    svg_out = datura.plot(ar[:,0], ar[:,1:])
    assert svg_out.split('points="')[1].split('"')[0] == '40.0,174.0 360.0,75.33333333333334 '

def test_np_two_x_two_y_column():
    ar = np.array([[1, 2], [-1, 1], [2, 1]]).T
    svg_out = datura.plot(np.hstack((ar[:, :1], ar[:, :1])), ar[:,1:])
    assert svg_out.split('points="')[1].split('"')[0] == '40.0,174.0 360.0,75.33333333333334 '