"""functions to produce a line plot"""
from datetime import datetime
import math
import textwrap
import os
import webbrowser
import warnings


def _interactive_display(filename):
    try:
        from IPython.display import SVG, display
        from IPython import get_ipython
        ipython_present = True
        try:
            shell = get_ipython().__class__.__name__
            if shell == 'ZMQInteractiveShell':
                in_notebook = True
                display(SVG(filename))
            elif shell == 'Shell':
                in_notebook = True
                display(SVG(filename))
            elif shell == 'TerminalInteractiveShell':
                in_notebook = False
            else:
                in_notebook = False
        except NameError:
            in_notebook = False
    except ModuleNotFoundError:
        in_notebook = False
        ipython_present = False
    if ipython_present and not in_notebook:
        webbrowser.open('file://' + os.path.realpath(filename))

    return in_notebook


def _check_equally_spaced(xs):
    unique_xs = list(set(xi for _x in xs for xi in _x))
    unique_xs.sort()
    diffs = set()
    for _i, xi in enumerate(unique_xs[:-1]):
        diff = unique_xs[_i + 1] - xi
        diffs.add(diff)

    return len(diffs) == 1, unique_xs


def _make_pretty_ticks(x_min, x_max, axis_is_time, xs):

    equally_spaced, unique_xs = _check_equally_spaced(xs)
    if axis_is_time:
        if len(unique_xs) <= 12:
            # if small number of x, just use them
            x_ticks_timestamps = unique_xs
        else:
            x_ticks_timestamps = [x_min, x_max]

        x_ticks = [datetime.fromtimestamp(_xt) for _xt in x_ticks_timestamps]
    else:
        if len(unique_xs) <= 10 and equally_spaced:
            # if small number of x and equally spaced, just use them
            x_ticks = unique_xs
            return x_ticks

        min_rounded = '{:.1e}'.format(x_min)
        max_rounded = '{:.1e}'.format(x_max)

        x_ticks = [float(min_rounded)]
        if min_rounded == max_rounded:
            if x_max > float(max_rounded):
                significand_st, exp_st = max_rounded.split("e")
                max_out = float(str(.1) + 'e' + exp_st) + float(max_rounded)
                x_ticks.append(max_out)
            if (x_min < float(min_rounded)) or (x_max == float(max_rounded)):
                significand_st, exp_st = min_rounded.split("e")
                min_out = float(str(-.1) + 'e' + exp_st) + float(min_rounded)
                x_ticks.insert(0, min_out)
        else:
            # add in more ticks if available
            mean = (float(max_rounded) + float(min_rounded)) / 2.
            thrd = (float(max_rounded) + float(min_rounded)) / 3.
            if float('{:.1e}'.format(mean)) == mean:
                x_ticks.append(float(mean))
                l_mean = (mean + float(min_rounded)) / 2.
                u_mean = (mean + float(max_rounded)) / 2.
                if float('{:.1e}'.format(l_mean)) == l_mean:
                    if float('{:.1e}'.format(u_mean)) == u_mean:
                        x_ticks.append(float(l_mean))
                        x_ticks.append(float(u_mean))
            elif float('{:.1e}'.format(thrd)) == thrd:
                if float('{:.1e}'.format(2*thrd)) == 2*thrd:
                    x_ticks.append(float(thrd))
                    x_ticks.append(2*float(thrd))
            x_ticks.append(float(max_rounded))
            x_ticks.sort()

    return x_ticks


def _strip_zeros(x_tick):
    if int(x_tick) == float(x_tick):
        x_out = str(int(x_tick))
    else:
        x_out = str(x_tick)
    return x_out


def _num2pretty_string(x_tick):
    if abs(x_tick) < 1000:
        x_out = _strip_zeros(x_tick)
    elif abs(x_tick) < 1000000:
        x_out = _strip_zeros(x_tick/1000) + 'K'
    elif abs(x_tick) < 1000000000:
        x_out = _strip_zeros(x_tick/1000000) + 'M'
    elif abs(x_tick) < 1000000000000:
        x_out = _strip_zeros(x_tick/1000000000) + 'B'
    else:
        x_out = "{:E}".format(x_tick)

    return x_out


def find_safe_time_trunc(x_ticks):
    unique_year = set()
    unique_month = set()
    unique_day = set()
    unique_hour = set()
    unique_minute = set()
    unique_second = set()
    unique_microsecond = set()
    for xt in x_ticks:
        unique_year.add(xt.year)
        unique_month.add(xt.month)
        unique_day.add(xt.day)
        unique_hour.add(xt.hour)
        unique_minute.add(xt.minute)
        unique_second.add(xt.second)
        unique_microsecond.add(xt.microsecond)

    all_same = [len(unique_year) == 1, len(unique_month) == 1,
                len(unique_day) == 1, len(unique_hour) == 1,
                len(unique_minute) == 1, len(unique_second) == 1,
                len(unique_microsecond) == 1]

    date_part = ['year', 'month', 'day', 'hour', 'minute', 'second', 'msecond']
    max_t_trunc = date_part[all_same.index(False)]
    min_t_trunc = date_part[::-1][all_same[::-1].index(False)]

    return max_t_trunc, min_t_trunc


def _tm2pretty_string(x_tick, max_t_trunc, min_t_trunc, n_ticks, isfirst):

    if n_ticks < 6 and min_t_trunc in ('year', 'month', 'day'):
        x_out = str(x_tick).split(' ')[0]
    elif min_t_trunc == 'year':
        x_out = str(x_tick.year)
    elif min_t_trunc == 'month' and max_t_trunc == 'year':
        x_out = str(x_tick.year) + '-' + str(x_tick.month)
    elif min_t_trunc == 'month' and max_t_trunc == 'month':
        x_out = x_tick.strftime("%B")[:3]
        if isfirst:
            x_out = str(x_tick.year) + '-' + x_tick.strftime("%B")[:3]
    elif min_t_trunc == 'day':
        x_out = str(x_tick).split(' ')[0]
    elif max_t_trunc in ('hour', 'minute', 'second', 'msecond'):
        x_out = str(x_tick).split(' ')[1]
    elif min_t_trunc in ('hour', 'minute'):
        x_out = ':'.join(str(x_tick).split(':')[0:2])
        if max_t_trunc in ('year', 'month', 'day'):
            x_out = '-'.join(x_out.split('-')[1:])
    else:
        x_out = str(x_tick)

    return x_out


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
    if xs is None:
        xs = [list(range(len(_y))) for _y in ys]  # convert to list of lists
    elif not all(isinstance(_x, list) for _x in xs):
        xs = [xs for i in range(len(ys))]  # convert to list of lists

    return xs, ys, yus, yls


def _convert_colors(colors, fill_colors, fill_opacities, ys, yus, CLR,
                    dark_mode):
    if colors is None:
        colors = [CLR, 'blue', 'red', 'green', 'orange', 'violet', 'brown']
        if len(ys) > len(colors):
            if dark_mode:
                num_colors = len(ys)
                colors = []
                for color_ind in range(num_colors):
                    blu = math.floor(min(255, color_ind*256*2/num_colors))
                    blu = 255 - blu
                    grn = math.floor(max(0, color_ind*256*2/num_colors - 256))
                    grn = 255 - grn
                    this_clr = 'rgb(255, ' + str(grn) + ', ' + str(blu) + ')'
                    colors.append(this_clr)
            else:
                num_colors = len(ys)
                colors = []
                for color_ind in range(num_colors):
                    red = math.floor(min(255, color_ind*256*2/num_colors))
                    grn = math.floor(max(0, color_ind*256*2/num_colors - 256))
                    this_color = 'rgb(' + str(red) + ', ' + str(grn) + ', 0)'
                    colors.append(this_color)
    if fill_colors is None:
        fill_colors = colors.copy()

    if (fill_opacities is None) and (yus is not None):
        if dark_mode:
            fill_opacities = ['0.4']*len(yus)
        else:
            fill_opacities = ['0.2']*len(yus)

    return colors, fill_colors, fill_opacities


def _make_x_axis(x_ticks, x_ticks_text, x_label, vb_width, vb_height, YBUF,
                 tick_length, x2vb, CLR):
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
                <text x="{xt_vb}" y="{x_axis_y_vb + tick_length}" fill="{CLR}"
                text-anchor="middle" dominant-baseline="hanging" > {xt_text}
                </text>""")

        x_axis_pts_vb += f""" {xtn_vb},{x_axis_yt_vb}"""
        x_axis_text_vb += '\n    '
        x_axis_text_vb += _remove_extra_whitespace(f"""\
            <text x="{xtn_vb}" y="{x_axis_y_vb + tick_length}" fill="{CLR}"
            text-anchor="middle" dominant-baseline="hanging" >
            {x_ticks_text[-1]} </text> </g>""")

        x_axis = _remove_extra_whitespace(f"""\
            <polyline fill="none" stroke="{CLR}" stroke-width="1"
            points="{x_axis_pts_vb}" />""")

    if x_label is None:
        x_axis_label = ''
    else:
        x_label_x_vb = .5*vb_width
        x_label_y_vb = vb_height - tick_length

        x_axis_label = _remove_extra_whitespace(f"""\
            <text x="{x_label_x_vb}" y="{x_label_y_vb}" fill="{CLR}"
            text-anchor="middle" font-family="sans-serif" font-size="10">
            {x_label} </text>""")

    return x_axis, x_axis_text_vb, x_axis_label


def _make_lines_and_labels(xs, ys, x2vb, y2vb, colors, labels, label_nudges,
                           tick_length, line_widths, points_radii):
    datalines = []
    all_circles = []
    if ys != []:
        for line_ind, y in enumerate(ys):
            x = xs[line_ind]

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
        else:
            c_r = 0
        if labels is not None:
            label = labels[line_ind]
            label_nudge = -1*label_nudges[line_ind]
            label_color = color
            x_label_vb = x2vb(max(xs[line_ind]))
            max_ind = xs[line_ind].index(max(xs[line_ind]))
            y_label_vb = y2vb(ys[line_ind][max_ind])
            line_labels += '\n    '
            line_labels += _remove_extra_whitespace(f"""\
                <text x="{x_label_vb + tick_length + c_r}"
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
                 tick_length, y2vb, CLR):

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
            yt_text = y_ticks_text[yt_ind]
            y_axis_pts_vb += _remove_extra_whitespace(f"""\
                {y_axis_xt_vb},{yt_vb}
                {y_axis_x_vb},{yt_vb}
                {y_axis_x_vb},{ytn_vb}""") + ' '
            y_axis_text_vb += '\n    '
            y_axis_text_vb += _remove_extra_whitespace(f"""\
                <text x="{y_axis_x_vb - tick_length}" y="{yt_vb}" fill="{CLR}"
                text-anchor="end" dominant-baseline="middle" > {yt_text}
                </text>""")

        y_axis_pts_vb += f"""{y_axis_xt_vb},{ytn_vb}"""
        y_axis_text_vb += _remove_extra_whitespace(f"""\
            <text x="{y_axis_x_vb - tick_length}" y="{ ytn_vb}" fill="{CLR}"
            text-anchor="end" dominant-baseline="middle" > {y_ticks_text[-1]}
            </text> </g>""")
        y_axis = _remove_extra_whitespace(f"""\
            <polyline fill="none" stroke="{CLR}" stroke-width="1"
            points="{y_axis_pts_vb}" />""")

    if y_label is None:
        y_axis_label = ''
    else:
        y_label_x_vb = tick_length
        y_label_y_vb = .5 * vb_height
        y_axis_label = _remove_extra_whitespace(f"""\
            <text fill="{CLR}" text-anchor="middle" dominant-baseline="hanging"
            transform="translate({y_label_x_vb},{y_label_y_vb}) rotate(270)"
            font-family="sans-serif" font-size="10"> {y_label} </text>""")

    return y_axis, y_axis_text_vb, y_axis_label


def _make_title(title, vb_width, tick_length, CLR):
    if title is None:
        title_vb = ''
    else:
        title_x_vb = .5*vb_width
        title_y_vb = tick_length
        title_vb = _remove_extra_whitespace(f"""\
            <text x="{title_x_vb}" y="{title_y_vb}" fill="{CLR}"
            text-anchor="middle" dominant-baseline="hanging"
            font-family="sans-serif" font-size="10"> {title} </text>""")
    return title_vb


def base_plot(xs, ys, yus=None, yls=None, filename='plot.svg',
              x_label=None, y_label=None, title=None,
              colors=None, fill_colors=None, fill_opacities=None,
              line_widths='1', points_radii=None,
              labels=None, label_nudges=None,
              x_ticks=None, y_ticks=None,
              x_ticks_text=None, y_ticks_text=None,
              interactive_mode=True, dark_mode=False):
    if filename[-4:] != '.svg':
        filename += '.svg'

    if x_ticks_text is not None:
        if x_ticks is None:
            warnings.warn('x_ticks_text requires x_ticks')
        elif len(x_ticks) != len(x_ticks_text):
            warnings.warn('#x_ticks != #x_ticks_text')

    if y_ticks_text is not None:
        if y_ticks is None:
            warnings.warn('y_ticks_text requires y_ticks')
        elif len(y_ticks) != len(y_ticks_text):
            warnings.warn('#y_ticks != #y_ticks_text')

    XBUF = 0.1
    YBUF = 0.13
    tick_length = 2
    vb_width = 400
    vb_height = 200

    vb_width_in = vb_width*.0096*2
    vb_height_in = vb_height*.0096*2

    if dark_mode:
        CLR = 'white'
    else:
        CLR = 'black'

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
        x_ticks = _make_pretty_ticks(x_min, x_max, x_axis_is_time, all_xs)

    if not x_axis_is_time and x_ticks_text is None:
        x_ticks_text = [_num2pretty_string(_xt) for _xt in x_ticks]
    if x_axis_is_time and len(x_ticks) >= 2:
        if x_ticks_text is None:
            max_t_trunc, min_t_trunc = find_safe_time_trunc(x_ticks)
            x_ticks_text = [_tm2pretty_string(_xt, max_t_trunc, min_t_trunc,
                                              len(x_ticks), _xt == x_ticks[0])
                            for _xt in x_ticks]
        # trying to convert ticks
        x_ticks = [datetime.timestamp(_xt) for _xt in x_ticks]

    if y_ticks is None:
        y_ticks = _make_pretty_ticks(y_min, y_max, False, all_ys)

    if type(labels) == str and len(ys) == 1:
        labels = [labels]  # convert to list with one string

    colors, fill_colors, fill_opacities = _convert_colors(colors, fill_colors,
                                                          fill_opacities, ys,
                                                          yus, CLR, dark_mode)

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
                                                        tick_length, x2vb,
                                                        CLR)
    if y_ticks_text is None:
        y_ticks_text = [_num2pretty_string(_yt) for _yt in y_ticks]
    y_axis, y_axis_text_vb, y_axis_label = _make_y_axis(y_ticks, y_ticks_text,
                                                        y_label, vb_width,
                                                        vb_height, XBUF,
                                                        tick_length, y2vb,
                                                        CLR)
    title_vb = _make_title(title, vb_width, tick_length, CLR)

    full_figure = textwrap.shorten(f"""\
    <?xml version="1.0" standalone="no"?>
    <svg width="{vb_width_in}in"
    height="{vb_height_in}in"
    viewBox="0 0 {vb_width} {vb_height}"
    xmlns="http://www.w3.org/2000/svg" version="1.1">""", 1000)

    if dark_mode:
        full_figure += '\n<rect width="100%" height="100%" fill="#000000"/>'

    full_figure += f'\n{polygons}\n{polylines}\n{line_labels}\n'
    full_figure += f'{x_axis}\n{x_axis_text_vb}\n{x_axis_label}\n'
    full_figure += f'{y_axis}\n{y_axis_text_vb}\n{y_axis_label}\n'
    full_figure += f'{title_vb}</svg>'

    out_file = open(filename, 'w')
    out_file.write(full_figure)
    out_file.close()

    if interactive_mode:
        in_notebook = _interactive_display(filename)

    return full_figure


def plot(*args, **kwargs):
    """Returns .svg text and saves a .svg file containing a line plot of the
    data in lists xs and ys.

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
        If list with one element, will result in no x-axis being displayed
        (but axis will be extended if necessary to include that value)
        If None an automatically generated axis is displayed
    y_ticks : list, optional
        locations of ticks on the y-axis.
        If list with one element, will result in no y-axis being displayed
        (but axis will be extended if necessary to include that value)
        If None an automatically generated axis is displayed
    x_ticks_text : list, optional
        text to replace x_tick labels (requires x_ticks)
    y_ticks_text : list, optional
        text to replace y_tick labels (requires y_ticks)
    interactive_mode : bool, optional
        if True, display inline (jupyter notebooks) or in new browser tab

    Returns
    -------
    full_figure : raw svg string

    Notes
    -----
    Tries to infer correct behavior when input is unexpected.

    """
    if len(args) == 1:
        xs = None
        ys = args[0]
    elif len(args) == 2:
        xs = args[0]
        ys = args[1]

    yus = kwargs.pop('yus', None)
    yls = kwargs.pop('yls', None)

    xs, ys, yus, yls = _convert_to_lists_of_lists(xs, ys, yus, yls)

    return base_plot(xs, ys, yus=yus, yls=yls, **kwargs)


def scatter(*args, **kwargs):
    """Returns .svg text and saves a .svg file containing a scatter plot of the
    data in lists xs and ys.

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
        If list with one element, will result in no x-axis being displayed
        (but axis will be extended if necessary to include that value)
        If None an automatically generated axis is displayed
    y_ticks : list, optional
        locations of ticks on the y-axis.
        If list with one element, will result in no y-axis being displayed
        (but axis will be extended if necessary to include that value)
        If None an automatically generated axis is displayed
    x_ticks_text : list, optional
        text to replace x_tick labels (requires x_ticks)
    y_ticks_text : list, optional
        text to replace y_tick labels (requires y_ticks)
    interactive_mode : bool, optional
        if True, display inline (jupyter notebooks) or in new browser tab

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
        kwargs['points_radii'] = [1]

    if len(args) == 1:
        xs = None
        ys = args[0]
    elif len(args) == 2:
        xs = args[0]
        ys = args[1]

    yus = kwargs.pop('yus', None)
    yls = kwargs.pop('yls', None)

    xs, ys, yus, yls = _convert_to_lists_of_lists(xs, ys, yus, yls)

    return base_plot(xs, ys, yus=yus, yls=yls, **kwargs)


def error_plot(*args, **kwargs):
    """Returns .svg text and saves a .svg file containing a line plot of the
    data in lists ys and xs with error patches between lists yus and yls.

    Parameters
    ----------
    xs : list of lists
        Abscissas of the lines to plot
        (each list corresponds to a different line)
    ys : list of lists
        Ordinates of the lines to plot
        (each list corresponds to a different line)
    yus : list of lists, optional
        Ordinates of the upper bounds of the error patches to plot
        (each list corresponds to a different line)
    yls : list of lists, optional
        Ordinates of the lower bounds of the error patches to plot
        (each list corresponds to a different line)
    y_errors: list of lists, optional
        Values to be added and subtracted from ys to create error patches
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
        If list with one element, will result in no x-axis being displayed
        (but axis will be extended if necessary to include that value)
        If None an automatically generated axis is displayed
    y_ticks : list, optional
        locations of ticks on the y-axis.
        If list with one element, will result in no y-axis being displayed
        (but axis will be extended if necessary to include that value)
        If None an automatically generated axis is displayed
    x_ticks_text : list, optional
        text to replace x_tick labels (requires x_ticks)
    y_ticks_text : list, optional
        text to replace y_tick labels (requires y_ticks)
    interactive_mode : bool, optional
        if True, display inline (jupyter notebooks) or in new browser tab

    Returns
    -------
    full_figure : raw svg string

    Notes
    -----
    Tries to infer correct behavior when input is unexpected.

    """

    xs, ys, yus, yls = _convert_to_lists_of_lists(args[0],
                                                  args[1],
                                                  kwargs.pop('yus', None),
                                                  kwargs.pop('yls', None))

    if yus is None or yls is None:
        y_errors = kwargs.pop('y_errors')
        y_errors = _convert_from_np_pd(y_errors)
        if y_errors is not None:
            if not all(isinstance(_y, list) for _y in y_errors):
                y_errors = [y_errors]  # convert to list of lists
        yus, yls = [], []
        for y_ind, y in enumerate(ys):
            yu = [yi + ye for yi, ye in zip(y, y_errors[y_ind])]
            yl = [yi - ye for yi, ye in zip(y, y_errors[y_ind])]
            yus.append(yu)
            yls.append(yl)

    return base_plot(xs, ys, yus=yus, yls=yls, **kwargs)


def hist(data, bin_edges=10, **kwargs):
    """Returns .svg text and saves a .svg file containing a histogram of the
    data in list of lists data.

    Parameters
    ----------
    data : list of lists
        raw values to be binned into histogram counts
        (each list corresponds to a different histogram)
    bin_edges : int or list of lists
        if int, that number of equally spaced bins are created between the
        minimum value in the data and the maximum value in data
        if lists, each list is used as bins for each list in the input data
    filename : string, optional
        Name of the file to save. Default is 'plot.svg'
    x_label : string, optional
        Label for x axis
    y_label : string, optional
        Label for y axis
    title : string, optional
        Title of figure
    colors : list, optional
        List containing svg colors for each histogram
    fill_colors : list, optional
        List containing svg fill colors for each patch
    fill_opacities : list, optional
        List containing numbers between 0 and 1 for each fill
    line_widths : list, optional
        List containing width for each histogram
    labels : list of strings, optional
        Labels corresponding to each line
    label_nudges : list of ints, optional
        distances to move labels (intended to manually avoid overlaps)
    x_ticks : list, optional
        locations of ticks on the x-axis.
        If list with one element, will result in no x-axis being displayed
        (but axis will be extended if necessary to include that value)
        If None an automatically generated axis is displayed
    y_ticks : list, optional
        locations of ticks on the y-axis.
        If list with one element, will result in no y-axis being displayed
        (but axis will be extended if necessary to include that value)
        If None an automatically generated axis is displayed
    x_ticks_text : list, optional
        text to replace x_tick labels (requires x_ticks)
    y_ticks_text : list, optional
        text to replace y_tick labels (requires y_ticks)
    interactive_mode : bool, optional
        if True, display inline (jupyter notebooks) or in new browser tab

        Returns
        -------
        full_figure : raw svg string

        Notes
        -----
        Tries to infer correct behavior when input is unexpected.

        """

    bin_edges, data, _, _ = _convert_to_lists_of_lists(bin_edges, data,
                                                       None, None)

    if max([len(be) for be in bin_edges]) == 1:
        num_bins = bin_edges[0][0]
        # user specified number of bins, not edges
        d_min = min([min(d) for d in data])
        d_max = max([max(d) for d in data])
        step = (d_max - d_min) / float(num_bins - 1)
        bin_edge_list = [d_min + i * step for i in range(num_bins)]
        bin_edges = [bin_edge_list for _d in data]

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


def bar(*args, bar_width=None, **kwargs):
    """Returns .svg text and saves a .svg file containing a bar chart of the
    data in lists xs and ys.

    Parameters
    ----------
    xs : list of lists, optional
        Abscissas of the centers of the bars to plot
        (each list corresponds to a different collection of bars)
        if not specified, bars are centered on 0, 1, ... N
    ys : list of lists
        Ordinates of the bars to plot
        (each list corresponds to a different collection)
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
    x_ticks : list, optional
        locations of ticks on the x-axis.
        If list with one element, will result in no x-axis being displayed
        (but axis will be extended if necessary to include that value)
        If None an automatically generated axis is displayed
    y_ticks : list, optional
        locations of ticks on the y-axis.
        If list with one element, will result in no y-axis being displayed
        (but axis will be extended if necessary to include that value)
        If None an automatically generated axis is displayed
    x_ticks_text : list, optional
        text to replace x_tick labels (requires x_ticks)
    y_ticks_text : list, optional
        text to replace y_tick labels (requires y_ticks)
    interactive_mode : bool, optional
        if True, display inline (jupyter notebooks) or in new browser tab

    Returns
    -------
    full_figure : raw svg string

    Notes
    -----
    Tries to infer correct behavior when input is unexpected.

    """
    if len(args) == 1:
        autoposition_bars = True
        xs = None
        ys = args[0]
    elif len(args) == 2:
        autoposition_bars = False
        xs = args[0]  # TODO check if xs is list of strings
        ys = args[1]
        if bar_width is None:
            bar_width = 0.8

    yus_in = kwargs.pop('yus', None)
    yls_in = kwargs.pop('yls', None)
    x_ticks = kwargs.pop('x_ticks', None)
    fill_opacities = kwargs.pop('fill_opacities', [1])

    xs, ys, _yus, _yls = _convert_to_lists_of_lists(xs, ys, None, None)

    if autoposition_bars and (bar_width is None):
        bar_width = 0.8 / len(xs)

    yus, yls = [], []
    for y_ind, y in enumerate(ys):
        yu = [yi*_i for yi in y for _i in (0, 1, 1, 0)]
        yl = [0 for yi in y for _i in (0, 1, 1, 0)]
        yus.append(yu)
        yls.append(yl)

    xts = set()
    xs_out = []
    for x_ind, x in enumerate(xs):
        bar_center = (-.5 * (len(xs) - 1) + x_ind) * bar_width
        nudges = [-.5*bar_width, -.5*bar_width, .5*bar_width, .5*bar_width]
        if autoposition_bars:
            nudges = [bar_center + _n for _n in nudges]
            xts = xts.union(set(x))
        xs_out.append([xi+_d for xi in x for _d in nudges])

    if x_ticks is None and autoposition_bars:
        x_ticks = list(xts)

    return base_plot(xs_out, ys=[], yus=yus, yls=yls, x_ticks=x_ticks,
                     fill_opacities=fill_opacities, **kwargs)
