"""functions to produce a line plot"""
from datetime import datetime
import math
import textwrap


def _make_pretty_ticks(x_min, x_max, xs):

    x_ticks = [x_min, x_max]

    return x_ticks


def _remove_extra_whitespace(in_string):
    in_string = ' '.join(in_string.split())
    return in_string


def _convert_from_np_pd(input_to_convert):
    """tries to convert from numpy array or pandas dataframe
    to list of lists"""
    if input_to_convert is not None:
        if type(input_to_convert) is not list:
            try:
                # convert from numpy array
                input_to_convert = input_to_convert.T.tolist()
            except AttributeError:
                try:
                    # convert from pandas dataframe
                    input_to_convert = input_to_convert.values.T.tolist()
                except AttributeError:
                    # make singletons into a list of length 1
                    input_to_convert = [input_to_convert]

    return input_to_convert


def _convert_to_lists_of_lists(xs, ys, yus, yls):
    """convert from numpy arrays, pandas dataframes, and lists"""
    ys = _convert_from_np_pd(ys)
    if not all(isinstance(_y, list) for _y in ys):
        ys = [ys]  # convert to list of lists

    yus = _convert_from_np_pd(yus)
    if yus is not None:
        if not all(isinstance(_y, list) for _y in yus):
            yus = [yus]  # convert to list of lists

    yls = _convert_from_np_pd(yls)
    if yls is not None:
        if not all(isinstance(_y, list) for _y in yls):
            yls = [yls]  # convert to list of lists

    xs = _convert_from_np_pd(xs)
    if not all(isinstance(_x, list) for _x in xs):
        xs = [xs for i in range(len(ys))]  # convert to list of lists

    return xs, ys, yus, yls


def _convert_colors(colors, fill_colors, fill_opacities, ys, yus):
    if colors is None:
        colors = ['black', 'blue', 'red', 'green', 'orange', 'violet', 'brown']
        if len(ys) > len(colors):
            num_colors = len(ys)
            colors = []
            for color_ind in range(num_colors):
                red = math.floor(min(255, color_ind*256*2/num_colors))
                green = math.floor(max(0, color_ind*256*2/num_colors - 256))
                this_color = 'rgb(' + str(red) + ', ' + str(green) + ', 0)'
                colors.append(this_color)
    if fill_colors is None:
        fill_colors = colors.copy()

    if (fill_opacities is None) and (yus is not None):
        fill_opacities = ['0.2']*len(yus)

    return colors, fill_colors, fill_opacities


def _make_x_axis(x_ticks, x_ticks_text, x_label, vb_width, vb_height, YBUF,
                 tick_length, x2vb):
    if len(x_ticks) < 2:
        x_axis = ''
        x_axis_text_vb = ''
    else:
        x_axis_y_vb = vb_height * (1 - YBUF) + 2 * tick_length
        x_axis_yt_vb = vb_height * (1 - YBUF) + tick_length

        x_axis_pts_vb = ''
        x_axis_text_vb = '<g font-family="sans-serif" font-size="10" >'
        for xt_ind, xt in enumerate(x_ticks[:-1]):
            xt_vb = x2vb(xt)
            xtn_vb = x2vb(x_ticks[xt_ind + 1])
            xt_text = x_ticks_text[xt_ind]
            x_axis_pts_vb += _remove_extra_whitespace(f"""\
                {xt_vb},{x_axis_yt_vb}
                {xt_vb},{x_axis_y_vb}
                {xtn_vb},{x_axis_y_vb}""") + ' '
            x_axis_text_vb += '\n    '
            x_axis_text_vb += _remove_extra_whitespace(f"""\
                <text x="{xt_vb}" y="{x_axis_y_vb + tick_length}" fill="black"
                text-anchor="middle" dominant-baseline="hanging" > {xt_text}
                </text>""")

        x_axis_pts_vb += f""" {xtn_vb},{x_axis_yt_vb}"""
        x_axis_text_vb += '\n    '
        x_axis_text_vb += _remove_extra_whitespace(f"""\
            <text x="{xtn_vb}" y="{x_axis_y_vb + tick_length}" fill="black"
            text-anchor="middle" dominant-baseline="hanging" >
            {x_ticks_text[-1]} </text> </g>""")

        x_axis = _remove_extra_whitespace(f"""\
            <polyline fill="none" stroke="black" stroke-width="1"
            points="{x_axis_pts_vb}" />""")

    if x_label is None:
        x_axis_label = ''
    else:
        x_label_x_vb = .5*vb_width
        x_label_y_vb = vb_height - tick_length

        x_axis_label = _remove_extra_whitespace(f"""\
            <text x="{x_label_x_vb}" y="{x_label_y_vb}" fill="black"
            text-anchor="middle" font-family="sans-serif" font-size="10">
            {x_label} </text>""")

    return x_axis, x_axis_text_vb, x_axis_label


def _make_lines_and_labels(xs, ys, x2vb, y2vb, colors, labels, label_nudges,
                           tick_length, line_widths, points_radii):
    datalines = []
    all_circles = []
    for line_ind, x in enumerate(xs):
        y = ys[line_ind]

        assert len(x) == len(y), 'all xs and ys should be the same length'

        x_vb = [x2vb(xi) for xi in x]
        y_vb = [y2vb(yi) for yi in y]
        dataline = ''
        circles = '<g fill="{cc}" stroke="none" stroke-width="0">'
        for xy_vb in zip(x_vb, y_vb):
            dataline += str(xy_vb[0]) + ',' + str(xy_vb[1]) + ' '
            circles += f'<circle cx="{xy_vb[0]}" cy="{xy_vb[1]}"'
            circles += ' r="{cr}"/>'

        circles += '</g>'
        datalines.append(dataline)
        all_circles.append(circles)

    polylines = ''
    line_labels = '<g font-family="sans-serif" font-size="10" >'
    for line_ind, dataline in enumerate(datalines):
        color = colors[line_ind % len(colors)]
        if line_widths is not None:
            line_w = line_widths[line_ind % len(line_widths)]
            polylines += f'<polyline fill="none" stroke="{color}" '
            polylines += f'stroke-width="{line_w}" points="{dataline}" />\n'
        if points_radii is not None:
            c_r = points_radii[line_ind % len(points_radii)]
            polylines += all_circles[line_ind].format(cr=c_r, cc=color) + '\n'
        if labels is not None:
            label = labels[line_ind]
            label_nudge = -1*label_nudges[line_ind]
            label_color = color
            x_label_vb = x2vb(max(xs[line_ind]))
            max_ind = xs[line_ind].index(max(xs[line_ind]))
            y_label_vb = y2vb(ys[line_ind][max_ind])
            line_labels += '\n    '
            line_labels += _remove_extra_whitespace(f"""\
                <text x="{x_label_vb + tick_length}"
                y="{y_label_vb}" dy="{label_nudge}" fill="{label_color}"
                dominant-baseline="middle">{label}</text>""")

    line_labels += '</g>'
    return polylines, line_labels


def _make_polygons(xs, yus, yls, x2vb, y2vb, fill_colors, fill_opacities):
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
            fill_color = fill_colors[line_ind % len(fill_colors)]
            fill_opacity = fill_opacities[line_ind % len(fill_opacities)]
            polygons += _remove_extra_whitespace(f"""\
                <polygon fill="{fill_color}" stroke="none"
                stroke-width="0" fill-opacity="{fill_opacity}"
                points="{dataline}" />""")
            polygons += '\n'
    return polygons


def _make_y_axis(y_ticks, y_ticks_text, y_label, vb_width, vb_height, XBUF,
                 tick_length, y2vb):

    if len(y_ticks) < 2:
        y_axis = ''
        y_axis_text_vb = ''
    else:
        y_axis_x_vb = vb_width * XBUF - 2 * tick_length
        y_axis_xt_vb = vb_width * XBUF - tick_length

        y_axis_pts_vb = ''
        y_axis_text_vb = '<g font-family="sans-serif" font-size="10" >'
        for yt_ind, yt in enumerate(y_ticks[:-1]):
            yt_vb = y2vb(yt)
            ytn_vb = y2vb(y_ticks[yt_ind + 1])
            y_axis_pts_vb += _remove_extra_whitespace(f"""\
                {y_axis_xt_vb},{yt_vb}
                {y_axis_x_vb},{yt_vb}
                {y_axis_x_vb},{ytn_vb}""") + ' '
            y_axis_text_vb += '\n    '
            y_axis_text_vb += _remove_extra_whitespace(f"""\
                <text x="{y_axis_x_vb - tick_length}" y="{yt_vb}" fill="black"
                text-anchor="end" dominant-baseline="middle" > {yt} </text>""")

        y_axis_pts_vb += f"""{y_axis_xt_vb},{ytn_vb}"""
        y_axis_text_vb += _remove_extra_whitespace(f"""\
            <text x="{y_axis_x_vb - tick_length}" y="{ ytn_vb}" fill="black"
            text-anchor="end" dominant-baseline="middle" > {y_ticks[-1]}
            </text> </g>""")
        y_axis = _remove_extra_whitespace(f"""\
            <polyline fill="none" stroke="black" stroke-width="1"
            points="{y_axis_pts_vb}" />""")

    if y_label is None:
        y_axis_label = ''
    else:
        y_label_x_vb = tick_length
        y_label_y_vb = .5 * vb_height
        y_axis_label = _remove_extra_whitespace(f"""\
            <text fill="black" text-anchor="middle" dominant-baseline="hanging"
            transform="translate({y_label_x_vb},{y_label_y_vb}) rotate(270)"
            font-family="sans-serif" font-size="10"> {y_label} </text>""")

    return y_axis, y_axis_text_vb, y_axis_label


def _make_title(title, vb_width, tick_length):
    if title is None:
        title_vb = ''
    else:
        title_x_vb = .5*vb_width
        title_y_vb = tick_length
        title_vb = _remove_extra_whitespace(f"""\
            <text x="{title_x_vb}" y="{title_y_vb}" fill="black"
            text-anchor="middle" dominant-baseline="hanging"
            font-family="sans-serif" font-size="10"> {title} </text>""")
    return title_vb


def base_plot(xs, ys, yus=None, yls=None, filename='plot.svg',
              x_label=None, y_label=None, title=None,
              colors=None, fill_colors=None, fill_opacities=None,
              line_widths='1', points_radii=None,
              labels=None, label_nudges=None,
              x_ticks=None, y_ticks=None):
    if filename[-4:] != '.svg':
        filename += '.svg'

    XBUF = 0.1
    YBUF = 0.13
    tick_length = 2
    vb_width = 400
    vb_height = 200

    vb_width_in = vb_width*.0096*2
    vb_height_in = vb_height*.0096*2

    xs, ys, yus, yls = _convert_to_lists_of_lists(xs, ys, yus, yls)

    if label_nudges is None and labels is not None:
        label_nudges = [0 for y in ys]

    line_widths = _convert_from_np_pd(line_widths)
    points_radii = _convert_from_np_pd(points_radii)

    x_ticks = _convert_from_np_pd(x_ticks)
    if x_ticks is not None:
        x_ticks.sort()

    y_ticks = _convert_from_np_pd(y_ticks)
    if y_ticks is not None:
        y_ticks.sort()

    x_axis_is_time = False
    for x_index, _x in enumerate(xs):
        try:
            _x[0] / 2
        except TypeError:
            x_axis_is_time = True
            xs[x_index] = [datetime.timestamp(_xi) for _xi in _x]

    all_xs = xs
    if x_ticks is None:
        all_xs = xs
    else:
        if x_axis_is_time:
            x_ticks_for_min_max = [datetime.timestamp(_xt) for _xt in x_ticks]
            all_xs = xs + [x_ticks_for_min_max]
        else:
            all_xs = xs + [x_ticks]

    x_min = min([min(x) for x in all_xs])
    x_max = max([max(x) for x in all_xs])

    if yus is None and yls is None:
        all_ys = ys
    else:
        all_ys = ys + yus + yls

    if y_ticks is not None:
        all_ys = all_ys + [y_ticks]

    y_min = min([min(y) for y in all_ys])
    y_max = max([max(y) for y in all_ys])

    if x_ticks is None:
        x_ticks = _make_pretty_ticks(x_min, x_max, xs)
        if x_axis_is_time:
            x_ticks = [datetime.fromtimestamp(_xt) for _xt in x_ticks]

    x_ticks_text = [str(_xt) for _xt in x_ticks]
    if x_axis_is_time and len(x_ticks) >= 2:
        x_ticks_text = [str(_xt).split(' ')[0] for _xt in x_ticks]
        # trying to convert ticks
        x_ticks = [datetime.timestamp(_xt) for _xt in x_ticks]

    if y_ticks is None:
        y_ticks = _make_pretty_ticks(y_min, y_max, ys)

    if type(labels) == str and len(ys) == 1:
        labels = [labels]  # convert to list with one string

    colors, fill_colors, fill_opacities = _convert_colors(colors, fill_colors,
                                                          fill_opacities, ys,
                                                          yus)

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
        # reflect to account for top-left origin in svg
        y_sc = 1 - ((y - y_min) / y_range)
        return y_sc * vb_height * (1 - 2 * YBUF) + (vb_height * YBUF)

    polylines, line_labels = _make_lines_and_labels(xs, ys, x2vb, y2vb, colors,
                                                    labels, label_nudges,
                                                    tick_length, line_widths,
                                                    points_radii)

    polygons = _make_polygons(xs, yus, yls, x2vb, y2vb,
                              fill_colors, fill_opacities)

    x_axis, x_axis_text_vb, x_axis_label = _make_x_axis(x_ticks, x_ticks_text,
                                                        x_label, vb_width,
                                                        vb_height, YBUF,
                                                        tick_length, x2vb)
    y_ticks_text = []  # TODO
    y_axis, y_axis_text_vb, y_axis_label = _make_y_axis(y_ticks, y_ticks_text,
                                                        y_label, vb_width,
                                                        vb_height, XBUF,
                                                        tick_length, y2vb)
    title_vb = _make_title(title, vb_width, tick_length)

    full_figure = textwrap.shorten(f"""\
    <?xml version="1.0" standalone="no"?>
    <svg width="{vb_width_in}in"
    height="{vb_height_in}in"
    viewBox="0 0 {vb_width} {vb_height}"
    xmlns="http://www.w3.org/2000/svg" version="1.1">""", 1000)

    full_figure += f'\n{polygons}\n{polylines}\n{line_labels}\n'
    full_figure += f'{x_axis}\n{x_axis_text_vb}\n{x_axis_label}\n'
    full_figure += f'{y_axis}\n{y_axis_text_vb}\n{y_axis_label}\n'
    full_figure += f'{title_vb}</svg>'

    out_file = open(filename, 'w')
    out_file.write(full_figure)
    out_file.close()

    return full_figure


def plot(*args, **kwargs):
    """Returns .svg text and saves a .svg file containing a plot of the data in
    lists ys and xs.

    Parameters
    ----------
    xs : list of lists
        Abscissas of the lines to plot
        (each list corresponds to a different line)
    ys : list of lists
        Ordinates of the lines to plot
        (each list corresponds to a different line)
    filename : string, optional
        Name of the file to save. Default is 'plot.svg'
    x_label : string, optional
        Label for x axis
    y_label : string, optional
        Label for y axis
    title : string, optional
        Title of figure
    colors : list, optional
        List containing svg colors for each line
    line_widths : list, optional
        List containing width for each line
    points_radii : list, optional
        List containing size of circles at each data point
    labels : list of strings, optional
        Labels corresponding to each line
    label_nudges : list of ints, optional
        distances to move labels (intended to manually avoid overlaps)
    x_ticks : list, optional
        locations of ticks on the x-axis.
        Empty (or length 1 list) will result in no x-axis being displayed.
        If None a automatically generated axis is displayed
    y_ticks : list, optional
        locations of ticks on the y-axis.
        Empty (or length 1 list) will result in no y-axis being displayed.
        If None a automatically generated axis is displayed

    Returns
    -------
    full_figure : raw svg string

    Notes
    -----
    Tries to infer correct behavior when input is unexpected.

    """

    return base_plot(*args, **kwargs)


def scatter(*args, **kwargs):
    """Returns .svg text and saves a .svg file containing a plot of the data in
    lists ys and xs.

    Parameters
    ----------
    xs : list of lists
        Abscissas of the lines to plot
        (each list corresponds to a different line)
    ys : list of lists
        Ordinates of the lines to plot
        (each list corresponds to a different line)
    filename : string, optional
        Name of the file to save. Default is 'plot.svg'
    x_label : string, optional
        Label for x axis
    y_label : string, optional
        Label for y axis
    title : string, optional
        Title of figure
    colors : list, optional
        List containing svg colors for each line
    points_radii : list, optional
        List containing size of circles at each data point
    labels : list of strings, optional
        Labels corresponding to each line
    label_nudges : list of ints, optional
        distances to move labels (intended to manually avoid overlaps)
    x_ticks : list, optional
        locations of ticks on the x-axis.
        Empty (or length 1 list) will result in no x-axis being displayed.
        If None a automatically generated axis is displayed
    y_ticks : list, optional
        locations of ticks on the y-axis.
        Empty (or length 1 list) will result in no y-axis being displayed.
        If None a automatically generated axis is displayed

    Returns
    -------
    full_figure : raw svg string

    Notes
    -----
    Tries to infer correct behavior when input is unexpected.

    """
    if 'line_widths' not in kwargs.keys():
        kwargs['line_widths'] = None
    if 'points_radii' not in kwargs.keys():
        points_radii = [1]

    return base_plot(*args, **kwargs)


def error_plot(*args, **kwargs):
    """Returns .svg text and saves a .svg file containing a plot of the data in
    lists ys and xs.

    Parameters
    ----------
    xs : list of lists
        Abscissas of the lines to plot
        (each list corresponds to a different line)
    ys : list of lists
        Ordinates of the lines to plot
        (each list corresponds to a different line)
    yus : list of lists, optional
        Abscissas of the upper bounds of the error patches to plot
        (each list corresponds to a different line)
    yls : list of lists, optional
        Abscissas of the lower bounds of the error patches to plot
        (each list corresponds to a different line)
    filename : string, optional
        Name of the file to save. Default is 'plot.svg'
    x_label : string, optional
        Label for x axis
    y_label : string, optional
        Label for y axis
    title : string, optional
        Title of figure
    colors : list, optional
        List containing svg colors for each line
    fill_colors : list, optional
        List containing svg colors for each patch (between yus and yls)
    fill_opacities : list, optional
        List containing numbers between 0 and 1 for each patch
        (between yus and yls)
    line_widths : list, optional
        List containing width for each line
    points_radii : list, optional
        List containing size of circles at each data point
    labels : list of strings, optional
        Labels corresponding to each line
    label_nudges : list of ints, optional
        distances to move labels (intended to manually avoid overlaps)
    x_ticks : list, optional
        locations of ticks on the x-axis.
        Empty (or length 1 list) will result in no x-axis being displayed.
        If None a automatically generated axis is displayed
    y_ticks : list, optional
        locations of ticks on the y-axis.
        Empty (or length 1 list) will result in no y-axis being displayed.
        If None a automatically generated axis is displayed

    Returns
    -------
    full_figure : raw svg string

    Notes
    -----
    Tries to infer correct behavior when input is unexpected.

    """

    return base_plot(*args, **kwargs)


def hist(data, bin_edges=None, **kwargs):
    if bin_edges is None:
        # automatically create bin edges...
        pass
    bin_edges, data, _, _ = _convert_to_lists_of_lists(bin_edges, data,
                                                       None, None)

    xs, ys, yus, yls = [], [], [], []
    for hist_ind in range(len(data)):
        x, y, yl = _make_histogram_xys(data[hist_ind], bin_edges[hist_ind])
        xs.append(x)
        ys.append(y)
        yus.append(y)
        yls.append(yl)

    return plot(xs, ys, yus=yus, yls=yls, **kwargs)


def _make_histogram_xys(hist_data, bin_edges):

    hist_data.sort()
    bin_edges.sort()

    bin_counts = [0 for be in bin_edges]

    for bin_ind, bin_edge in enumerate(bin_edges):
        while len(hist_data) > 0 and hist_data[0] < bin_edge:
            bin_counts[bin_ind] += 1
            hist_data.pop(0)
    while len(hist_data) > 0 and hist_data[0] == bin_edges[-1]:
        # include right side of last bin to match numpy behavior
        bin_counts[bin_ind] += 1
        hist_data.pop(0)

    x_out = [be for be in bin_edges for _i in (1, 2)]
    y_out = [0] + [bc for bc in bin_counts[1:] for _i in (1, 2)] + [0]
    yl_out = [0 for y_o in y_out]

    return x_out, y_out, yl_out
