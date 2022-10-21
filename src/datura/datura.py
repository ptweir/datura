

def plot(xs, ys, yus=None, yls=None, filename='plot.svg',
        x_label=None, y_label=None, title=None,
        colors=['black', '#d32323', '#0073bb', '#41a700'],
        labels=None, label_nudges=None,
        x_ticks=None, y_ticks=None):
    """
    Create an .svg file containing a plot of the data in lists ys and xs
    """
    if filename[-4:] != '.svg':
        filename += '.svg'
    if label_nudges is None and labels is not None:
        label_nudges = [0 for y in ys]

    XBUF = 0.1
    YBUF = 0.13
    tick_length = 2
    vb_width = 400
    vb_height = 200

    vb_width_in = vb_width*.0096*2
    vb_height_in = vb_height*.0096*2

    # the following conditionals are just to account for what I expect to be common sources of confusion
    if type(xs) is not list:
        try:
            xs = xs.T.tolist() # convert from numpy array
        except:
            xs = xs.values.T.tolist() # convert from pandas dataframe

    if type(ys) is not list:
        try:
            ys = ys.T.tolist() # convert from numpy array
        except:
            ys = ys.values.T.tolist() # convert from pandas dataframe

    if not all(isinstance(_y, list) for _y in ys):
        ys = [ys] # convert to list of lists

    if not all(isinstance(_x, list) for _x in xs):
        xs = [xs for i in range(len(ys))]  # convert to list of lists

    x_min = min([min(x) for x in xs])
    x_max = max([max(x) for x in xs])

    if yus is None and yls is None:
        all_ys = ys
    else:
        all_ys = ys + yus + yls

    y_min = min([min(y) for y in all_ys])
    y_max = max([max(y) for y in all_ys])

    if x_ticks == 'auto':
        x_ticks = [x_min, x_max]
    if y_ticks == 'auto':
        y_ticks = [y_min, ymax]

    x_range = x_max - x_min
    if x_range == 0:
        x_range = 1.

    y_range = y_max - y_min
    if y_range == 0:
        y_range = 1.

    def x2vb(x):
        x_sc = (x - x_min) / x_range
        return x_sc * vb_width * (1 - 2 * XBUF) + (vb_width * XBUF)

    def y2vb(y):
        y_sc = 1 - ((y - y_min) / y_range) # reflect to account for top-left origin in svg
        return y_sc * vb_height * (1 - 2 * YBUF) + (vb_height * YBUF)

    datalines = []
    for line_ind, x in enumerate(xs):
        y = ys[line_ind]

        assert len(x) == len(y), 'all xs and ys should be the same length'

        x_vb = [x2vb(xi) for xi in x]
        y_vb = [y2vb(yi) for yi in y]
        dataline = ''
        for xy_vb in zip(x_vb, y_vb):
            dataline += str(xy_vb[0]) + ',' + str(xy_vb[1]) + ' '

        datalines.append(dataline)

    polylines = ''
    line_labels = '<g font-family="sans-serif" font-size="10" >'
    for line_ind, dataline in enumerate(datalines):
        color = colors[line_ind%len(colors)]
        polylines += f"""<polyline fill="none" stroke="{color}" stroke-width="1" points="{dataline}" />\n """
        if labels is not None:
            label = labels[line_ind]
            label_nudge = -1*label_nudges[line_ind]
            label_color = color
            x_label_vb = x2vb(max(xs[line_ind]))
            max_ind = xs[line_ind].index(max(xs[line_ind]))
            y_label_vb = y2vb(ys[line_ind][max_ind])
            line_labels += f""" <text x="{x_label_vb + tick_length}" y="{y_label_vb}" dy="{label_nudge}" fill="{label_color}" dominant-baseline="middle" > {label} </text>\n"""

    line_labels += '</g>'

    if yus is None:
        polygons = ''
    else:
        datalines = []
        for line_ind, x in enumerate(xs):
            yu = yus[line_ind]
            yl = yls[line_ind]
            x_vb = [x2vb(xi) for xi in x]
            yu_vb = [y2vb(yi) for yi in yu]
            yl_vb = [y2vb(yi) for yi in yl]
            dataline = ''
            for xyu_vb in zip(x_vb, yu_vb):
                dataline += str(xyu_vb[0]) + ',' + str(xyu_vb[1]) + ' '
            for xyl_vb in zip(x_vb[::-1], yl_vb[::-1]):
                dataline += str(xyl_vb[0]) + ',' + str(xyl_vb[1]) + ' '

            datalines.append(dataline)

        polygons = ''
        for line_ind, dataline in enumerate(datalines):
            color = colors[line_ind%len(colors)]
            polygons += f"""<polygon fill="{color}" stroke="none" stroke-width="0" fill-opacity="0.2" points="{dataline}" />\n """

    if x_ticks is None:
        x_axis = ''
        x_axis_text_vb = ''
    else:
        x_ticks.sort()
        x_axis_y_vb = vb_height * (1 - YBUF) + 2 * tick_length
        x_axis_yt_vb = vb_height * (1 - YBUF) + tick_length

        x_axis_pts_vb = ''
        x_axis_text_vb = '<g font-family="sans-serif" font-size="10" >'
        for xt_ind, xt in enumerate(x_ticks[:-1]):
            xt_vb = x2vb(xt)
            xtn_vb = x2vb(x_ticks[xt_ind + 1])
            x_axis_pts_vb += f"""{xt_vb},{x_axis_yt_vb} {xt_vb},{x_axis_y_vb} {xtn_vb},{x_axis_y_vb} """
            x_axis_text_vb += f""" <text x="{xt_vb}" y="{x_axis_y_vb + tick_length}" fill="black" text-anchor="middle" dominant-baseline="hanging" > {xt} </text>\n"""

        x_axis_pts_vb += f"""{xtn_vb},{x_axis_yt_vb}"""
        x_axis_text_vb += f""" <text x="{xtn_vb}" y="{x_axis_y_vb + tick_length}" fill="black" text-anchor="middle" dominant-baseline="hanging" > {x_ticks[-1]} </text> </g>"""
        x_axis = f"""<polyline fill="none" stroke="black" stroke-width="1" points="{x_axis_pts_vb}" />"""

    if x_label is None:
        x_axis_label = ''
    else:
        x_label_x_vb = .5*vb_width
        x_label_y_vb = vb_height - tick_length
        x_axis_label = f"""<text x="{x_label_x_vb}" y="{x_label_y_vb}" fill="black" text-anchor="middle" font-family="sans-serif" font-size="10"> {x_label} </text>"""


    if y_ticks is None:
        y_axis = ''
        y_axis_text_vb = ''
    else:
        y_ticks.sort()
        y_axis_x_vb = vb_width * XBUF - 2 * tick_length
        y_axis_xt_vb = vb_width * XBUF - tick_length

        y_axis_pts_vb = ''
        y_axis_text_vb = '<g font-family="sans-serif" font-size="10" >'
        for yt_ind, yt in enumerate(y_ticks[:-1]):
            yt_vb = y2vb(yt)
            ytn_vb = y2vb(y_ticks[yt_ind + 1])
            y_axis_pts_vb += f"""{y_axis_xt_vb},{yt_vb} {y_axis_x_vb},{yt_vb} {y_axis_x_vb},{ytn_vb} """
            y_axis_text_vb += f""" <text x="{y_axis_x_vb - tick_length}" y="{yt_vb}" fill="black" text-anchor="end" dominant-baseline="middle" > {yt} </text>\n"""

        y_axis_pts_vb += f"""{y_axis_xt_vb},{ytn_vb}"""
        y_axis_text_vb += f""" <text x="{y_axis_x_vb - tick_length}" y="{ ytn_vb}" fill="black" text-anchor="end" dominant-baseline="middle" > {y_ticks[-1]} </text> </g>"""
        y_axis = f"""<polyline fill="none" stroke="black" stroke-width="1" points="{y_axis_pts_vb}" />"""

    if y_label is None:
        y_axis_label = ''
    else:
        y_label_x_vb = tick_length
        y_label_y_vb = .5 * vb_height
        y_axis_label = f"""<text fill="black" text-anchor="middle" dominant-baseline="hanging" transform="translate({y_label_x_vb},{y_label_y_vb}) rotate(270)" font-family="sans-serif" font-size="10"> {y_label} </text>"""


    if title is None:
        title_vb = ''
    else:
        title_x_vb = .5*vb_width
        title_y_vb = tick_length
        title_vb = f"""<text x="{title_x_vb}" y="{title_y_vb}" fill="black" text-anchor="middle" dominant-baseline="hanging" font-family="sans-serif" font-size="10"> {title} </text>"""


    full_figure = f"""<?xml version="1.0" standalone="no"?>
    <svg width="{vb_width_in}in" height="{vb_height_in}in" viewBox="0 0 {vb_width} {vb_height}" 
    xmlns="http://www.w3.org/2000/svg" version="1.1">

    {polygons}
    {polylines}
    {line_labels}
    {x_axis}
    {x_axis_text_vb}
    {x_axis_label}
    {y_axis}
    {y_axis_text_vb}
    {y_axis_label}
    {title_vb}

    </svg>
    """

    out_file = open(filename, 'w')
    out_file.write(full_figure)
    out_file.close()

    return(full_figure)

"""
labels = ['black', 'red', 'blue', 'hi', 'hi']
label_nudges = [0, -2, 5, 0, 0]
x_label = 'x label'
y_label = 'y label'
title = 'Chart title'

x1 = [xx*.1 for xx in range(-100,101)]
xs = [x1, x1, x1]
#xs = [x1]

y1 = [(xx*.035)**3 for xx in range(-100,101)]
y2 = [(xx*.1)**2 for xx in range(-100,101)]
y3 = [int(str(xx**10)[:1]) + int(xx>0)*(xx*.1)**2 for xx in range(-100,101)]
ys = [y1, y2, y3]


yu1 = [y+10 for y in y1]
yl1 = [y-10 for y in y1]
yu2 = y2 # this is a bit of a hack
yl2 = y2
yu3 = [y*1.3+5 for y in y3]
yl3 = [y*.5-10 for y in y3]
yus = [yu1, yu2, yu3]
yls = [yl1, yl2, yl3]

plot(xs, ys, yus=yus, yls=yls, x_label='x label', y_label='y label', title='title',
labels=labels, label_nudges=label_nudges, x_ticks=[-5, -10, 0, 5, 10], y_ticks=[-50, 0, 50, 100])
"""